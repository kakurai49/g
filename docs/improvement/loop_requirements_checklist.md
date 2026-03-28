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
