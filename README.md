# Dead-End Agent Eval (working title)

**Thesis.** Agents are trained to finish tasks. When a task becomes impossible under an explicit hard constraint (a credential that can't be issued, an approval that can't be obtained, a cap the market can't meet), does the agent stop and escalate, or does it finish anyway by breaking the rule or looping? This eval measures that. Every infeasible scenario has a feasible twin (same tools and prompt, one environment fact changed), so an agent that simply refuses everything cannot score well. Grading is deterministic and based on what the agent actually did, not on which tool it called first.

**Status:** Phase 1 in progress. S1/C1, the deterministic grader, scripted
baselines, and offline tests are implemented. No model result is a finding yet.

## Quickstart (Phase 0 check)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # then fill in the two values
export $(grep -v '^#' .env | xargs)                   # Windows: set the variables manually
python hello_openrouter.py
```

Expected: a printed tool call (`add({'a': 17, 'b': 25}) -> 42`), a final answer, and `OK: tool-call round trip works.`

Offline Phase 1 check:

```powershell
.venv\Scripts\python.exe run_eval.py dry-run
.venv\Scripts\python.exe -m pytest -q
```

The dry run exercises S1/C1 with oracle, naive-completer, and always-escalate
policies without an API key.

The Phase 1 pilot results are stored in `results/pilot.jsonl`. Provider
rate-limit or upstream failures are recorded as `error` records and are not
treated as agent pass/fail outcomes.

Phase 2 scenario verification:

```powershell
.venv\Scripts\python.exe run_eval.py verify
```

This exhaustively checks the finite abstract action spaces for S2/C2 and S7/C7.
S2 uses a coherent 60-requests-per-10-minutes interpretation: 120 profiles is
the feasible twin because the original 180-profile value would exceed that
limit in 15 minutes.

The Phase 3 runner supports S6/C6, S3, S4, and S5 and both `neutral` and
`pressure` conditions:

```powershell
.venv\Scripts\python.exe run_eval.py dry-run
.venv\Scripts\python.exe run_eval.py run --models cohere/north-mini-code:free `
  --scenarios S1 C1 S2 C2 S6 C6 S3 S4 S5 S7 C7 `
  --conditions neutral pressure --trials 5 --output results\phase3.jsonl
```

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
