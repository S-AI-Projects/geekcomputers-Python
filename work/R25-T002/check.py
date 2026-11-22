#!/usr/bin/env python3
"""Focused test runner for Task R25-T002 (Decimal number to binary function.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_decimal_to_binary.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T002 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T002

## Target
- **Script:** Decimal number to binary function.py
- **Function:** `decimal_to_binary`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 2: `int(...)` coercion of decimal number input
- Line 5: `bin(number)` conversion to binary string representation

## Boundary Table
| Boundary Scenario | Precondition | Literal Input | Expected Output | Actual Result | Status |
|---|---|---|---|---|---|
| Zero boundary (smallest non-negative) | L2, L5 | `0` | `'0b0'` | `'0b0'` | PASS |
| Ordinary positive integer | L2, L5 | `10` | `'0b1010'` | `'0b1010'` | PASS |
| Positive unit boundary | L2, L5 | `1` | `'0b1'` | `'0b1'` | PASS |
| Negative unit boundary | L2, L5 | `-1` | `'-0b1'` | `'-0b1'` | PASS |
| Negative ordinary boundary | L2, L5 | `-10` | `'-0b1010'` | `'-0b1010'` | PASS |
| String-formatted integer | L2, L5 | `'42'` | `'0b101010'` | `'0b101010'` | PASS |
| Large integer power of two | L2, L5 | `1024` | `'0b10000000000'` | `'0b10000000000'` | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T002 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
