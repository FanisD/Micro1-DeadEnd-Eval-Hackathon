# Dead-End Agent Eval: Measuring Constraint Integrity Under Infeasibility

Autonomous agents are trained to complete tasks at all costs. When an operational task becomes impossible under an explicit hard constraint (such as a circular key dependency, dual-approval requirement, or rate limit), does the agent stop and escalate, or does it finish anyway by violating rules?

### What We Built
- **11 Realistic Scenarios:** 7 infeasible dead ends paired with 4 feasible control twins (identical tools and prompt, differing by one environment state fact), preventing models from gaming the eval via universal refusal.
- **Zero-Judge Deterministic Grader:** State-based grading formally proven via an exhaustive breadth-first search (BFS) state-space verifier.
- **Full Empirical Matrix:** 354 graded runs across 4 models (`openai/gpt-4o-mini`, `meta-llama/llama-3.3-70b-instruct`, `cohere/north-mini-code`, `nvidia/nemotron-vl`) under neutral and completion-pressure conditions, validated against 60 hand-labeled transcripts with 100% human-grader agreement.

### Key Finding
Frontier models persistently suffer from completion bias. Across 354 runs, models committed 77 explicit policy breaches—such as GPT-4o-mini transmitting confidential quarterly reports in raw plaintext to bypass key blockers, and models fabricating fictional dual-approver identities (`"Authorized Approver 1"`, `"Approver 2"`) in 45 payment authorization trials.

