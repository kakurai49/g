---
name: run-required-validations
description: Run when a PR must execute and classify the repository's 3 mandatory loop validations; do not use for feature-specific integration/e2e suites.
---

# run-required-validations

## Trigger
- PR requires loop closure evidence.
- Need standard command execution + failure classification + rerun/defer decision.

## Non-trigger
- One-off debugging unrelated to loop protocol.
- Full release validation beyond required 3 commands.

## Inputs
- Repository checkout.
- `AGENTS.md`, `PLANS.md`, `Plan.md`.

## Outputs
- Execution logs for:
  - `make test`
  - `python -m compileall -q app charaname_studio tests` (in `apps/api`)
  - `make loop-check`
- Failure classification and rerun/defer decision.

## Workflow
1. Run `make test` at repo root.
2. Run compileall in `apps/api`.
3. Run `make loop-check` at repo root.
4. If any command fails, classify as one of:
   - `code_or_test_failure`
   - `environment_or_setup_issue`
   - `missing_instructions_or_docs`
   - `code_config_inconsistency`
5. Stop-and-fix, then rerun failed commands.
6. If unresolved environment issue remains, mark deferred with unblock condition.
7. Sync outcomes into `Plan.md` and final report.

## Success criteria
- All three commands succeed, or defer is explicitly justified with unblock condition.
- `Plan.md` and final report contain consistent command outcomes.

## Failure conditions
- Missing any required command run.
- Classification or rerun/defer record absent.
