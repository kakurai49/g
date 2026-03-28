#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_FILES = [
    "AGENTS.md",
    "PLANS.md",
    "Plan.md",
    "docs/improvement/skills.md",
    "docs/improvement/loop_requirements_checklist.md",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED_FILES if not (root / p).exists()]

    if missing:
        print("loop-check: missing required files:")
        for item in missing:
            print(f"- {item}")
        return 1

    plans_text = (root / "PLANS.md").read_text(encoding="utf-8")
    plan_text = (root / "Plan.md").read_text(encoding="utf-8")

    if "Plan.md" not in plans_text:
        print("loop-check: PLANS.md must define Plan.md writing rules")
        return 1
    if "Validation result log" not in plan_text:
        print("loop-check: Plan.md must contain Validation result log section")
        return 1

    print("loop-check: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
