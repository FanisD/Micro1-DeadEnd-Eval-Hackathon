# Running notes

Log surprising model behavior, harness bugs, and scenario ambiguities as you find them. This feeds the findings section and the video. One dated line per entry.

- 2026-11-01: repo skeleton created.
- 2026-11-02: Phase 1 pilot completed 30 configured runs across S1/C1,
  neutral condition, three free OpenRouter model slugs. Nemotron completed all
  10 runs. Cohere completed 8/10 and produced plaintext-leak failures on S1;
  Dots failed provider requests on all 10 runs after retries. Provider errors
  are recorded separately from graded agent outcomes.
