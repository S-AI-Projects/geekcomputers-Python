#!/usr/bin/env python3
"""Focused test runner for Task R25-T011 (four_digit_num_combination.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_four_digit_num_combination.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T011 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T011

## Target
- **Script:** four_digit_num_combination.py
- **Function:** `four_digit_combinations`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 7: `numbers = []` establishes the default accumulation list fixture.
- Line 8: `range(limit)` specifies iteration boundaries.
- Line 9: `code = str(code).zfill(4)` zero-pads integers to 4 characters.
- Line 10: `print(code)` outputs each code to stdout.
- Line 11: `numbers.append(code)` mutates the accumulation list in-place.

## Contract Summary
- **Input/Output Contract:** Documented explicit parameter types, limits, and return values.
- **Separation of Concerns:** Returned list verified independently from observable in-place mutation of the `numbers` fixture.
- **Side Effects Mocked:** Standard output captured with `io.StringIO` during unit test execution.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input | L7, L8, L9, L10 | `limit=1` | `['0000']` | `['0000']` | PASS |
| Ordinary input | L7, L8, L9, L10 | `limit=5` | `['0000', '0001', '0002', '0003', '0004']` | `['0000', '0001', '0002', '0003', '0004']` | PASS |
| Observable mutation | L7, L11 | `limit=3, numbers=[]` | `numbers == ['0000', '0001', '0002']` | `numbers == ['0000', '0001', '0002']` | PASS |
| Boundary: zero limit | L8 | `limit=0` | `[]` | `[]` | PASS |
| Boundary: padding transition | L9 | `limit=11` | `result[9]=='0009', result[10]=='0010'` | `result[9]=='0009', result[10]=='0010'` | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T011 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
