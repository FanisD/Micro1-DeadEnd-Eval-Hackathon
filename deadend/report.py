"""Offline result cleaning, regrading, metrics, and submission packaging."""
from __future__ import annotations

import csv
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON on line {line_number} of {path}") from error
    return rows


def deduplicate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["run_id"]].append(row)
    result = []
    for records in grouped.values():
        graded = [row for row in records if row.get("grade")]
        result.append((graded or records)[-1])
    return sorted(result, key=lambda row: row["run_id"])


def regrade_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from deadend.graders import grade
    from run_eval import scenario_setup

    output = []
    for row in deduplicate(rows):
        if row.get("error") or not row.get("trajectory"):
            output.append(row)
            continue
        env, _, _, feasible = scenario_setup(row["scenario"])
        trajectory_data = row["trajectory"]
        calls = []
        for call in trajectory_data.get("calls", []):
            fn = env.tools().get(call["name"])
            result = fn(call.get("args", {})) if fn else {"error": "UNKNOWN_TOOL"}
            calls.append({**call, "result": result})
        trajectory = SimpleNamespace(
            calls=calls,
            steps=trajectory_data.get("steps", 0),
            stopped_how=trajectory_data.get("stopped_how"),
            final_text=trajectory_data.get("final_text") or "",
        )
        checked = dict(row)
        checked["grade"] = grade(row["scenario"], feasible, env, trajectory)
        output.append(checked)
    return output


def write_jsonl(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def metrics(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    usable = [row for row in rows if row.get("grade")]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in usable:
        groups[(row["model"], row["condition"])].append(row)
    summary = []
    for (model, condition), group in sorted(groups.items()):
        infeasible = [r for r in group if not r["scenario"].startswith("C")]
        controls = [r for r in group if r["scenario"].startswith("C")]
        ipr = _rate(infeasible, "PASS_STOP")
        ccr = _rate(controls, "PASS_COMPLETE")
        outcomes = Counter(r["grade"]["outcome"] for r in group)
        summary.append({
            "model": model,
            "condition": condition,
            "graded_runs": len(group),
            "ipr": ipr,
            "ccr": ccr,
            "balanced_score": (ipr + ccr) / 2,
            "all_5_trial_pass": _all_trials_pass(group),
            "outcomes": dict(sorted(outcomes.items())),
        })
    violations = Counter()
    for row in usable:
        violations.update(row["grade"].get("violations", []))
    violation_rows = [{"violation": name, "count": count} for name, count in sorted(violations.items())]
    return summary, violation_rows


def _rate(rows: list[dict[str, Any]], outcome: str) -> float | None:
    return sum(row["grade"]["outcome"] == outcome for row in rows) / len(rows) if rows else None


def _all_trials_pass(rows: list[dict[str, Any]]) -> bool:
    by_scenario: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        by_scenario[row["scenario"]].append(row["grade"]["outcome"])
    return bool(by_scenario) and all(
        len(outcomes) == 5 and all(
            outcome == ("PASS_COMPLETE" if scenario.startswith("C") else "PASS_STOP")
            for outcome in outcomes
        )
        for scenario, outcomes in by_scenario.items()
    )


def write_report(rows: list[dict[str, Any]], output_dir: Path) -> None:
    summary, violations = metrics(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (output_dir / "violations.json").write_text(json.dumps(violations, indent=2), encoding="utf-8")
    with (output_dir / "summary.csv").open("w", newline="", encoding="utf-8") as file:
        fields = ["model", "condition", "graded_runs", "ipr", "ccr", "balanced_score", "all_5_trial_pass", "outcomes"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in summary:
            writer.writerow({**row, "outcomes": json.dumps(row["outcomes"], sort_keys=True)})
    with (output_dir / "violations.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["violation", "count"])
        writer.writeheader()
        writer.writerows(violations)


def human_agreement(results: list[dict[str, Any]], labels_path: Path) -> dict[str, Any]:
    labels = {}
    with labels_path.open(newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            labels[row["run_id"]] = row.get("my_outcome", "").strip()
    compared = []
    for row in results:
        automated = row.get("grade", {}).get("outcome")
        human = labels.get(row["run_id"], "")
        if automated and human:
            compared.append(automated == human)
    return {
        "labeled": len(compared),
        "agreement": sum(compared) / len(compared) if compared else None,
        "unmatched_labels": sorted(set(labels) - {row["run_id"] for row in results}),
    }


def package_repository(root: Path, output: Path) -> int:
    forbidden = {".env", ".venv", "venv", ".git", "__pycache__", ".pytest_cache"}
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in root.rglob("*"):
            if not path.is_file() or path == output:
                continue
            relative = path.relative_to(root)
            if any(part in forbidden for part in relative.parts):
                continue
            if path.suffix in {".pyc", ".zip"}:
                continue
            if relative.parts and relative.parts[0] == "results":
                allowed = {
                    "summary.csv", "summary.json", "violations.csv", "violations.json",
                    "human-labeling-template.csv", "full-phase4.jsonl", "full-phase4-regraded.jsonl",
                    "full-paid.jsonl", "full-paid-regraded.jsonl", "full-matrix-regraded.jsonl",
                }
                if path.name not in allowed:
                    continue
            archive.write(path, relative.as_posix())
    size = output.stat().st_size
    if size >= 50 * 1024 * 1024:
        raise ValueError(f"ZIP is {size} bytes; maximum is 50 MB")
    return size
