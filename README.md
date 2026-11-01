# Dead-End Agent Eval (working title)

**Thesis.** Agents are trained to finish tasks. When a task becomes impossible under an explicit hard constraint (a credential that can't be issued, an approval that can't be obtained, a cap the market can't meet), does the agent stop and escalate, or does it finish anyway by breaking the rule or looping? This eval measures that. Every infeasible scenario has a feasible twin (same tools and prompt, one environment fact changed), so an agent that simply refuses everything cannot score well. Grading is deterministic and based on what the agent actually did, not on which tool it called first.

**Status:** Phase 0 skeleton. No scenarios or results yet. Nothing here should be read as a finding.

## Quickstart (Phase 0 check)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # then fill in the two values
export $(grep -v '^#' .env | xargs)                   # Windows: set the variables manually
python hello_openrouter.py
```

Expected: a printed tool call (`add({'a': 17, 'b': 25}) -> 42`), a final answer, and `OK: tool-call round trip works.`

## Layout

```
README.md
requirements.txt
.env.example               # never commit .env
hello_openrouter.py        # Phase 0 tool-call round-trip check
run_eval.py                # CLI: run | regrade | dry-run | verify (stub for now)
deadend/
  scenarios/               # one YAML per scenario (Phase 1+)
  envs/                    # one env module per scenario family
tests/                     # golden trajectories + grader tests
results/                   # recorded JSONL transcripts + summaries
docs/
  phase0-checklist.md      # steps only you can do
  instructions-capture.md  # fill in from the HackerRank Instructions tab
  notes.md                 # running notes on surprising model behavior
```

## Rules this repo follows

- Synthetic data only. No employer or client data.
- API keys only via environment variables. Never in the ZIP.
- Submission format is whatever the HackerRank Instructions tab says; this layout adapts to it.
