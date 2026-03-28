# PLANS.md

`Plan.md` operational standard for this repository.

## Order rule
- Always read this file before creating or editing `Plan.md`.

## Required sections in `Plan.md`
1. Goal
2. Non-goals
3. Milestones (small, testable units)
4. Acceptance criteria (per milestone)
5. Validation commands (per milestone)
6. Status (todo / in_progress / done / deferred)
7. Validation result log (`command`, `exit code`, `summary`, `rerun`)
8. Defer log (`reason`, `unblock condition`, `owner`)
9. Decision log
10. Current status
11. Next action

## Milestone granularity
- Prefer one milestone per reviewable change set.
- Keep each milestone independently verifiable.

## Validation writing standard
- Record exact command text.
- Record UTC timestamp and exit code.
- If failed, apply stop-and-fix and rerun.

## Stop-and-fix and rerun
- Do not proceed to next milestone while required validation is failing.
- Rerun the same command after fixes and log both attempts.

## Defer policy
- Allowed only when blocked by environment/setup constraints.
- Must include concrete unblock condition and follow-up action.

## Living document principle
- `Plan.md` must reflect current reality, not intent only.
- Update `Current status` and `Next action` at the end of each loop.
