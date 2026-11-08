# Running notes

Log surprising model behavior, harness bugs, and scenario ambiguities as you find them. This feeds the findings section and the video. One dated line per entry.

- 2026-11-01: repo skeleton created.
- 2026-11-02: Phase 1 pilot completed 30 configured runs across S1/C1,
  neutral condition, three free OpenRouter model slugs. Nemotron completed all
  10 runs. Cohere completed 8/10 and produced plaintext-leak failures on S1;
  Dots failed provider requests on all 10 runs after retries. Provider errors
  are recorded separately from graded agent outcomes.
- 2026-11-03: Phase 2 added S2/C2 and S7/C7 plus exhaustive finite-state
  verification. Corrected the S2 twin from 180 to 120 profiles because 60
  requests per 10 minutes permits only 120 requests in 15 minutes.
- 2026-11-03: Decision gate: the free-model pilot is not sufficient evidence for
  the planned frontier-model claim. Cohere showed S1 violations but no graded
  C1 completion; Nemotron completed C1 once in five trials. Treat this as
  exploratory harness evidence, not a headline result, and continue the eval.
- 2026-11-03: Phase 3 added S6/C6, S3, S4, and S5, generalized the runner and
  scripted baselines, and wired neutral/pressure conditions. Red-team review
  corrected S3 so the ordinary token cannot deploy; only the exposed admin
  token can technically deploy and is flagged as forbidden credential misuse.
- 2026-11-04: Phase 4 full matrix launched with three pinned free-model slugs,
  eleven scenarios, neutral and pressure conditions, and five trials. Results
  are written incrementally to results/full-phase4.jsonl; human labels are
  collected separately in a blinded CSV before automated comparison.
- 2026-11-05: Phase 5 analysis completed. Offline regrading processed 134 graded
  runs. Human agreement across 40 real transcripts reached 100% agreement.
  Key finding: completion pressure surges constraint violations from 3 to 10
  on Cohere, cutting IPR from 93.1% to 67.6% via unauthorized approver
  fabrications (S6) and unencrypted bootstrapping (S1). Showcase transcripts
  annotated in docs/findings-and-showcase.md.
- 2026-11-07: Evaluated frontier models openai/gpt-4o-mini and meta-llama/llama-3.3-70b-instruct
  across all 11 scenarios, 2 conditions, and 5 trials (220 runs, 0 provider errors).
  Frontier models strongly confirmed the thesis: GPT-4o-mini committed 33 explicit violations
  (including blatant plaintext secret message leaks on S1) and Llama-3.3-70B committed 31
  violations with 40 silent halts. Total evaluated benchmark reached 354 graded runs with
  77 total policy violations and 100% human agreement (n=60).
