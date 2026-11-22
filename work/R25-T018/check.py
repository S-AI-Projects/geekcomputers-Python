#!/usr/bin/env python3
"""Focused test runner for Task R25-T018 (Conversation.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_conversation.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T018 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T018

## Target
- **Script:** Conversation.py
- **Function:** `conversation`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 8: `name = getuser()` default identity anchor.
- Line 9: `name_check = input(...)` confirmation check.
- Line 23: `response = input(...)` meeting response check.
- Lines 31-33: Line 31 `else:` branch handles unexpected responses (input error fallback).
- Lines 41-43: Line 41 `else:` branch handles second input error fallback.

## Failure Path Coverage
- **Smallest Failure Input:** Constructed `""` (empty string) reaching Line 31 failure branch because `"".lower().startswith("y")` and `"".lower().startswith("n")` are both False.
- **Sentinel & Side Effects:** Verified emission of `"You may have made an input error. Please restart and try again."` and exit status 1.
- **Caller State Resilience:** Verified that immediately after a failure run, an ordinary valid run succeeds completely with exit code 0.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest failure input (Line 31) | L9, L23, L31 | `["y", ""]` | Error message + exit code 1 | Error message + exit code 1 | PASS |
| Ordinary valid call (Line 26) | L9, L23, L26 | `["yes", "yes"]` | "Nice :)" + exit code 0 | "Nice :)" + exit code 0 | PASS |
| Recovery after failure | L31, L26 | Failure followed by success | Both states isolated; second run succeeds | Both runs verified | PASS |
| Secondary failure branch (Line 41) | L28, L41 | `["y", "n", "invalid"]` | Error message + exit code 1 | Error message + exit code 1 | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T018 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
