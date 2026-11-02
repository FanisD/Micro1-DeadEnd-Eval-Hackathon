# Instructions-tab capture sheet

Fill this in while reading the challenge's Instructions tab. Paste exact wording where it matters (weights, format rules). The plan's assumptions are listed so you can mark where reality differs.

## Rubric (scored out of 100)
| Criterion | Weight | Exact wording / notes |
| Significance | Not numerically published | Target a real, practical limitation rather than a gotcha; clear frontier-model failures are valued. |
| Clarity & Accuracy | Not numerically published | Tasks should be clear and unambiguous with a defensible grading standard; 5–10 tasks recommended. |
| Grader Reliability | Not numerically published | The automated grader should avoid false passes and false fails. |
| Originality & Reproducibility | Not numerically published | Work must be original and reproducible, and explain why models fail. |

## Submission format
- Required ZIP structure (folders, file names, entry-point script): Exactly one
  code-only ZIP, maximum 50 MB. Do not include confidential employer/client data
  or the video.
- README requirements: Explain how to run and reproduce the eval, the grading
  standard, and the meaningful reason models fail.
- Required results file or format (JSON? CSV? specific schema?):
- Video: length, hosting, anything specific it must show: Short video walkthrough;
  provide its link separately and do not package it in the ZIP.
- Description: length limit and what it should cover: Short description; no strict
  character or word count was provided.

## Reference materials / starter tools
- Starter template or framework provided? (Plan assumes none is required; says custom harness is fine)
- Reference example evals (list them, note their format):
- Any required task or grader interface:

## Constraints that could affect the plan
| Plan assumption | What the Instructions say | Action |
|---|---|---|
| Custom Python harness over OpenRouter is allowed | No strict language/runtime restrictions; README must explain execution and reproduction. | Keep the Python harness. |
| 11 scenarios (7 infeasible + 4 twins) is acceptable | 5–10 tasks are recommended; no maximum was stated. | Keep the planned set, but Tier 1 remains the fallback. |
| Deterministic code grader, no LLM judge in the headline | Reliable automated grading is prioritized. | Keep deterministic grading. |
| Scripted/offline `regrade` mode is fine for reproducibility | Reproducibility is explicitly prioritized. | Keep offline regrading. |
| Synthetic environments (no real services) are fine | Confidential employer/client data is prohibited; no real-service requirement was stated. | Keep synthetic data and document it. |
| Models to test: any, at my own cost | No model restriction was stated. | Keep OpenRouter and document tested models. |
| Anything about trick/gotcha, originality, or disclosure of prior work | Real limitation, not gotcha; work must be original and reproducible. | Keep the related-work and originality disclosures. |

## Deadline and logistics
- Submission closes (check the exact time shown on the challenge page): Public event
  page says November 9, 2026 at 05:15 GMT; confirm in HackerRank.
- Where the submission is made, and whether it can be edited before the deadline:
  HackerRank challenge submission; the FAQ says the latest complete resubmission
  before the deadline is evaluated.
- Questions to email hackathon@micro1.ai: hackathon@micro1.ai

## Surprises
Confirmed by the authenticated Instructions tab: one code-only ZIP under 50 MB,
separate short-video link, short description, unrestricted language/runtime, and
the four judging priorities above. No conflicts with eval-plan.md were found.
