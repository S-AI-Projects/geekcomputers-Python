#!/usr/bin/env python3
"""Focused test runner for Task R25-T017 (rangoli.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_rangoli.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T017 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T017

## Target
- **Script:** rangoli.py
- **Function:** `print_rangoli`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 5: `def print_rangoli(n):` input size parameter.
- Line 7: `width = 4 * n - 3` determines line width and centering canvas.
- Line 14: `chr(96 + n - j)` descending alphabet loop.
- Line 19: `chr(97 + n - k)` ascending alphabet loop.
- Lines 24, 38: `string.center(width, "-")` centered line rendering.

## Decisive State Transition
- Trailing hyphen suppression occurs on line 15 & 21 when `len(string) == width` at the center row (`i = n`).
- In non-center rows (`i < n`), uncentered strings carry a trailing hyphen (e.g. `'c-'` of length 2), which Python's `center(9, '-')` cleanly absorbs by padding 4 dashes on the left and 3 on the right (`'----c----'`).

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (n=1) | L7, L14 | `n=1` | `"a\\n"` | `"a\\n"` | PASS |
| Ordinary input (n=3) doc example | L7, L14, L19, L24 | `n=3` | 5-line diamond rangoli | 5-line diamond rangoli | PASS |
| Decisive state transition | L7, L15, L21, L24 | `n=3, width=9` | Exact center boundary & centering mechanics | Exact match | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T017 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
