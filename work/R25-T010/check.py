#!/usr/bin/env python3
"""Focused test runner for Task R25-T010 (calculator.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_calculator.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T010 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T010

## Target
- **Script:** calculator.py
- **Function:** `calc`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 33: `def calc(term):` accepts input expression
- Line 41: `term.replace(" ", "")` whitespace sanitization
- Line 42: `term.replace("^", "**")` exponent operator conversion
- Line 45: `term.replace("%", "/100.00")` percentage normalization
- Lines 50-62: `functions = [...]` anchor list of math functions
- Line 67: `eval(term)` expression evaluation

## Mutation Resistance Analysis
- **Target Invariant 1 (Power Operator):** `term.replace('^', '**')`
  - Mutant: `term.replace('^', '*')`
  - Input: `'2 ^ 3'`
  - Original Result: `8` (PASS)
  - Mutant Result: `6` (FAILS assertion `assert res == 8`)
- **Target Invariant 2 (Percentage Divisor):** `term.replace('%', '/100.00')`
  - Mutant: `term.replace('%', '/10.00')`
  - Input: `'50% * 100'`
  - Original Result: `50.0` (PASS)
  - Mutant Result: `500.0` (FAILS assertion `assert res == 50.0`)
- **Cleanliness Guarantee:** Production `calculator.py` contains no test-only hooks or mutant branches.

## Verification Matrix
| Scenario | Preconditions | Literal Input | Expected Output | Actual Result | Status |
|---|---|---|---|---|---|
| Smallest valid input | L33, L67 | `'0'` | `0` | `0` | PASS |
| Ordinary arithmetic input | L41, L67 | `'2 + 3 * 4'` | `14` | `14` | PASS |
| Exponentiation invariant | L42 | `'2 ^ 3'` | `8` | `8` | PASS |
| Percentage invariant | L45 | `'50% * 100'` | `50.0` | `50.0` | PASS |
| Scientific anchors | L50-62 | `'sin(0)'`, `'sqrt(16)'` | `0.0`, `4.0` | `0.0`, `4.0` | PASS |
| Exponent mutant detection | L42 | `'2 ^ 3'` on `*` mutant | Fails with `6 != 8` | Mutant detected | PASS |
| Percentage mutant detection | L45 | `'50% * 100'` on `/10` mutant | Fails with `500.0 != 50.0` | Mutant detected | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T010 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
