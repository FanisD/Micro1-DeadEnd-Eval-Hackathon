import json
from pathlib import Path
from types import SimpleNamespace

from deadend.report import deduplicate, human_agreement, metrics, package_repository, read_jsonl, write_jsonl


def record(run_id, model, scenario, outcome=None, error=None):
    row = {"run_id": run_id, "model": model, "scenario": scenario, "condition": "neutral", "trial": 1}
    if outcome:
        row["grade"] = {"outcome": outcome, "violations": []}
    if error:
        row["error"] = error
    return row


def test_deduplicate_prefers_graded_record():
    rows = [
        record("r1", "m", "S1", error="provider"),
        record("r1", "m", "S1", outcome="PASS_STOP"),
    ]
    result = deduplicate(rows)
    assert len(result) == 1
    assert result[0]["grade"]["outcome"] == "PASS_STOP"


def test_metrics_excludes_provider_errors():
    rows = [
        record("s1", "m", "S1", "PASS_STOP"),
        record("c1", "m", "C1", "PASS_COMPLETE"),
        record("e1", "m", "S1", error="provider"),
    ]
    summary, _ = metrics(rows)
    assert summary[0]["graded_runs"] == 2
    assert summary[0]["ipr"] == 1.0
    assert summary[0]["ccr"] == 1.0


def test_jsonl_round_trip(tmp_path: Path):
    path = tmp_path / "rows.jsonl"
    rows = [record("r", "m", "S1", "PASS_STOP")]
    write_jsonl(rows, path)
    assert read_jsonl(path) == rows


def test_package_excludes_secrets_and_virtualenv(tmp_path: Path):
    (tmp_path / ".env").write_text("SECRET=x", encoding="utf-8")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "secret.txt").write_text("x", encoding="utf-8")
    (tmp_path / "README.md").write_text("ok", encoding="utf-8")
    output = tmp_path / "out.zip"
    package_repository(tmp_path, output)
    names = __import__("zipfile").ZipFile(output).namelist()
    assert names == ["README.md"]


def test_human_agreement(tmp_path: Path):
    labels = tmp_path / "labels.csv"
    labels.write_text("run_id,my_outcome\nr1,PASS_STOP\n", encoding="utf-8")
    assert human_agreement([record("r1", "m", "S1", "PASS_STOP")], labels)["agreement"] == 1.0
