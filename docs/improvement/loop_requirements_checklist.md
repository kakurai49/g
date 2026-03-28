# loop requirements checklist

## Execution checklist (per PR)
- [x] Read `PLANS.md` before creating/updating `Plan.md`.
- [x] Added/updated task milestones in `Plan.md` with acceptance criteria, validation commands, and status.
- [x] Updated `docs/improvement/skills.md` in the same PR as `AGENTS.md` creation/update.
- [x] Updated this checklist with loop-closure learnings.
- [x] Ran required validations and reflected outcomes in `Plan.md` and final report.
- [x] Re-ran failed validations after fixes, or documented defer reason and unblock condition.

## Required validations
- `make test`
- `python -m compileall -q app charaname_studio tests` (run in `apps/api`)
- `make loop-check`

## Latest loop notes (2026-03-28 due diligence)
- `make test` initially failed with missing `httpx` in the active Python environment.
- Failure category applied: `environment_or_setup_issue`.
- Resolution used stop-and-fix: installed `apps/api` dependencies, then reran all required validations successfully.

## Latest loop notes (2026-03-28 translation update)
- Translated `AGENTS.md`, `PLANS.md`, and `Plan.md` into Japanese while preserving loop structure.
- `make test` failed once due to missing `httpx`; categorized as `environment_or_setup_issue`.
- Applied stop-and-fix by installing `apps/api` dependencies and reran required validations successfully.
