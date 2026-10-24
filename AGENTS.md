# AGENTS.md: system constitution

## Project
Second Look (crack triage): phone-photo triage (Low, Medium, High) of cracks in structural elements of buildings that nobody inspects.
Read `spec/constitution/mission.md`, `roadmap.md` and `tech_stack.md` before changing anything.

## Non-negotiable rules
1. The tool never issues a permit, a clearance or a "safe" guarantee.
2. Any doubt goes to an expert: unusable photo means retake, low model confidence means "Expert needed". Low confidence must never become Low risk.
3. Low risk is earned: usable image, confident model, and the risk matrix says Low.
4. An engineer confirms every High and every referral.
5. Triage levels come from written, auditable rules in `src/triage/`, not from a language model.
6. Language models are probabilistic and do not understand loads or materials. Verify outputs against data and tests.
7. Do not invent data, citations or numbers. Mark assumptions as "assumption" and thresholds as "illustrative until calibrated".

## Working method
- Spec-driven: write or update the spec in `spec/` first, then code in `src/`, then tests in `tests/`.
- Every feature needs a test. Compare against the non-AI baseline (an engineer's visual check) where relevant.
- Keep sessions short. Record decisions in this file or in `spec/`.
- Never commit personal photos or raw datasets. Keep them in `data/` (ignored).

## Commands
- Tests: `pytest`
