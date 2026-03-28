.PHONY: test loop-check

test:
	cd apps/api && pytest -q --cov=app --cov-report=term-missing --cov-fail-under=85

loop-check:
	python scripts/loop_check.py
