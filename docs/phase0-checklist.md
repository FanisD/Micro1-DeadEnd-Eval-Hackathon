# Phase 0 checklist: steps only you can do (~1.5 h)

Do them in this order. The first two decide whether the rest of the plan changes.

## 1. Join the challenge (10 min)
- [x] Open the event page: https://www.hackerrank.com/event/micro1-eval-hackathon
- [x] Use the direct challenge link from the **Event Details** section (registration is closed, so this is the way in). The page also lists https://hr.gs/micro1-eval-hackathon
- [x] Complete the onboarding form (profile links and background)
- [x] Accept the micro1 Participant Agreement

## 2. Read the Instructions tab (30 min)
- [x] Open the challenge's **Instructions** tab and fill in `docs/instructions-capture.md` as you read
- [x] Skim the optional teaching material and reference examples (cap at 30 min)
- [x] Anything that contradicts `eval-plan.md` wins. No conflicts were found.

## 3. Community (5 min)
- [x] Join the Discord linked on the event page and check for official clarifications

## 4. OpenRouter (15 min)
- [ ] Create an account at openrouter.ai (manual)
- [ ] **Set a spend limit** on the key (suggestion: start at $20, raise it after the pilot gives a real cost estimate) (manual)
- [ ] Create an API key (manual)
- [ ] On the models page, filter for models that support tools and pick one cheap or free model for development. Put its slug in `.env` (manual)
- [x] Keep the key out of chat, screenshots, and git. It lives only in `.env` or your shell

## 5. Local setup (20 min)
- [x] Unzip the skeleton and `cd` into it
- [x] `git init`, then a first commit
- [x] Create a venv, `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env` and fill in both values (manual; do not send the key in chat)
- [ ] Run `python hello_openrouter.py` (blocked until OpenRouter is configured)
- [x] Run `pip freeze` and pin the exact versions in `requirements.txt`

## Exit criteria
- You know the required ZIP format and the rubric.
- The skeleton is on your machine and committed.
- `hello_openrouter.py` prints a tool call and ends with `OK: tool-call round trip works.`

Current status: all challenge and local setup items are complete except the
OpenRouter account/key/model configuration and the live hello-world run.
