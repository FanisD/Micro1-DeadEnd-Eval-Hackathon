# Instructions-tab capture sheet

Fill this in while reading the challenge's Instructions tab. Paste exact wording where it matters (weights, format rules). The plan's assumptions are listed so you can mark where reality differs.

## Rubric (scored out of 100)
| Criterion | Weight | Exact wording / notes |
|---|---|---|
| | | |
| | | |
| | | |
| | | |

## Submission format
- Required ZIP structure (folders, file names, entry-point script): One code-only ZIP,
  maximum 50 MB. Do not include the video in the ZIP.
- README requirements:
- Required results file or format (JSON? CSV? specific schema?):
- Video: length, hosting, anything specific it must show: Short video walkthrough;
  the public FAQ says the link must be accessible without permission and play with
  audio.
- Description: length limit and what it should cover: Short description required;
  exact limit is not visible on the public event page.

## Reference materials / starter tools
- Starter template or framework provided? (Plan assumes none is required; says custom harness is fine)
- Reference example evals (list them, note their format):
- Any required task or grader interface:

## Constraints that could affect the plan
| Plan assumption | What the Instructions say | Action |
|---|---|---|
| Custom Python harness over OpenRouter is allowed | Public FAQ: languages/runtimes are unrestricted if documented. | Keep the Python harness. |
| 11 scenarios (7 infeasible + 4 twins) is acceptable | Public FAQ recommends 5–10 tasks and has no maximum. | Prefer Tier 1 if the final count is a concern. |
| Deterministic code grader, no LLM judge in the headline | Not specified publicly. | Confirm in the Instructions tab. |
| Scripted/offline `regrade` mode is fine for reproducibility | Reproducibility is required for a strong eval. | Keep it; confirm required interface in the Instructions tab. |
| Synthetic environments (no real services) are fine | Public rules prohibit confidential employer/client data; no contrary requirement found. | Keep synthetic data and document it. |
| Models to test: any, at my own cost | Public FAQ suggests free/low-cost models and frontier models. | Keep OpenRouter; confirm any model restrictions. |
| Anything about trick/gotcha, originality, or disclosure of prior work | Must be original; copying benchmarks without disclosure is cheating. | Add related work and disclose borrowed material. |

## Deadline and logistics
- Submission closes (check the exact time shown on the challenge page): Public event
  page says November 9, 2026 at 05:15 GMT; confirm in HackerRank.
- Where the submission is made, and whether it can be edited before the deadline:
  HackerRank challenge submission; the FAQ says the latest complete resubmission
  before the deadline is evaluated.
- Questions to email hackathon@micro1.ai: hackathon@micro1.ai

## Surprises
Public pages confirm the ZIP/video/description requirements and the 5–10-task
recommendation, but the exact scoring rubric and required ZIP entry points remain
unverified until the HackerRank Instructions tab is opened while authenticated.
