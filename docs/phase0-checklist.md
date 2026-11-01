# Phase 0 checklist: steps only you can do (~1.5 h)

Do them in this order. The first two decide whether the rest of the plan changes.

## 1. Join the challenge (10 min)
- [ ] Open the event page: https://www.hackerrank.com/event/micro1-eval-hackathon
- [ ] Use the direct challenge link from the **Event Details** section (registration is closed, so this is the way in). The page also lists https://hr.gs/micro1-eval-hackathon
- [ ] Complete the onboarding form (profile links and background)
- [ ] Accept the micro1 Participant Agreement

## 2. Read the Instructions tab (30 min)
- [ ] Open the challenge's **Instructions** tab and fill in `docs/instructions-capture.md` as you read
- [ ] Skim the optional teaching material and reference examples (cap at 30 min)
- [ ] Anything that contradicts `eval-plan.md` wins. Note it, then tell me and I'll update the plan

## 3. Community (5 min)
- [ ] Join the Discord linked on the event page and check for official clarifications

## 4. OpenRouter (15 min)
- [ ] Create an account at openrouter.ai
- [ ] **Set a spend limit** on the key (suggestion: start at $20, raise it after the pilot gives a real cost estimate)
- [ ] Create an API key
- [ ] On the models page, filter for models that support tools and pick one cheap or free model for development. Put its slug in `.env`
- [ ] Keep the key out of chat, screenshots, and git. It lives only in `.env` or your shell

## 5. Local setup (20 min)
- [ ] Unzip the skeleton and `cd` into it
- [ ] `git init`, then a first commit
- [ ] Create a venv, `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env` and fill in both values
- [ ] Run `python hello_openrouter.py`
- [ ] Once it works, run `pip freeze` and pin the exact versions in `requirements.txt` (the current file only has lower bounds)

## Exit criteria
- You know the required ZIP format and the rubric.
- The skeleton is on your machine and committed.
- `hello_openrouter.py` prints a tool call and ends with `OK: tool-call round trip works.`

If the hello-world fails, paste me the full error (with the key removed) and the model slug you used. The usual causes are a model that doesn't support tool calling, a missing key, or a spend limit of $0.
