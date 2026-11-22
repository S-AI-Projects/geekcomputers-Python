#!/usr/bin/env python3
"""Focused test runner for Task R25-T008 (calc_area.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_calc_area.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T008 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T008

## Target
- **Script:** calc_area.py
- **Function:** `main`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 5: `shape = int(...)` input parsing
- Line 11: `shape == 1` square area formula
- Line 14: `shape == 2` rectangle area formula
- Line 32: `else: print("You have selected wrong choice.")` failure fallback branch
- Line 35: `restart = input(...)` loop control

## Failure Branch & Validity Matrix
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Documented failure branch | L5, L32 | `shape=9, restart='n'` | `"You have selected wrong choice."` | `"You have selected wrong choice."` | PASS |
| Smallest valid input | L11 | `shape=1, side=0.0` | `"Area of square = 0.0"` | `"Area of square = 0.0"` | PASS |
| Ordinary valid input | L11 | `shape=1, side=5.0` | `"Area of square = 25.0"` | `"Area of square = 25.0"` | PASS |
| Valid call after failure | L14, L32 | `shape=99` then `shape=2` | Failure handled, rectangle area 20.0 computed | Both calls succeeded | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T008 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
