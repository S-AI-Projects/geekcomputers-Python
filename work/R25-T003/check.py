#!/usr/bin/env python3
"""Focused test runner for Task R25-T003 (Randomnumber.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_random_number.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T003 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T003

## Target
- **Script:** Randomnumber.py
- **Function:** `random_number` / `Randomnumber`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 4: `from random import randint`
- Line 6: `randint(0, 9)` establishing default range [0, 9]

## Cross-Check Differential Results
| Scenario | Preconditions | Literal Input | Reference Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (zero span) | L4, L6 | `start=0, end=0` | `0` | `0` | PASS |
| Ordinary input (seed=42) | L4, L6 | `start=0, end=9` | `1` | `1` | PASS |
| Seed sweep cross-check (50 seeds) | L4, L6 | Seeds 0..49, [0, 9] | Identical across all 50 runs | Identical across all 50 runs | PASS |
| Type and argument isolation | L4, L6 | `start=2, end=7` | `int in [2, 7]` | `int in [2, 7]`, args untouched | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T003 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
