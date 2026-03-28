# AGENTS.md

## Repo map
- `apps/api/`: FastAPI service (`app/`) and pytest suite (`tests/`).
- `docs/`: architecture/operations guidance and improvement logs.
- `scripts/`: helper shell/python scripts.
- `.github/workflows/`: CI/CD definitions.
- `Makefile`: local validation entrypoints (`make test`, `make loop-check`).

## Mandatory execution order (loop protocol)
1. Read `AGENTS.md` and then **`PLANS.md`**.
2. Create/update `Plan.md` using `PLANS.md` rules.
3. Implement minimal scoped changes.
4. Update `docs/improvement/skills.md` and `docs/improvement/loop_requirements_checklist.md`.
5. Run required validations and record outcomes in `Plan.md`.

## Required validation commands
- `make test`
- `python -m compileall -q app charaname_studio tests`
- `make loop-check`

Run `python -m compileall -q app charaname_studio tests` from `apps/api/` so the expected paths resolve.

## Validation failure categories (must log in `Plan.md`)
1. `code_or_test_failure`
2. `environment_or_setup_issue`
3. `missing_instructions_or_docs`
4. `code_config_inconsistency`

## Stop-and-fix / defer rule
- Default: stop and fix, then rerun the same command.
- Defer allowed only for `environment_or_setup_issue` that cannot be resolved in this PR.
- Every defer must include reason, unblock condition, and owner in `Plan.md`.

## Done definition for loop/bootstrap PRs
A PR that creates/updates `AGENTS.md` must also update, in the same PR:
- `PLANS.md`
- `Plan.md`
- `docs/improvement/skills.md`
- `docs/improvement/loop_requirements_checklist.md`
- validation logs for the 3 required commands.
