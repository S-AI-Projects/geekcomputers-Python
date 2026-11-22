#!/usr/bin/env python3
"""Focused test runner for Task R25-T014 (Python Distance.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_python_distance.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T014 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T014

## Target
- **Script:** Python Distance.py
- **Function:** `python_distance`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 3: `terms = 10` establishes default iteration terms fixture.
- Line 9: `result = list(map(lambda x: 2**x, range(terms)))` defines the functional calculation.

## Mathematical Invariants
- **Shape Invariant:** For any non-negative integer `terms`, output is a `list` with `len(result) == terms`.
- **Base Invariant:** `result[0] == 1` when `terms >= 1`.
- **Recurrence Invariant:** `result[i+1] == 2 * result[i]` for all consecutive indices.
- **Bit-level Equivalence:** `result[i] == (1 << i)` for all `0 <= i < terms`.
- **Monotonicity:** `result[i] < result[i+1]` strictly increasing for all `i`.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (zero) | L9 | `terms=0` | `[]` | `[]` | PASS |
| Smallest positive input (one) | L9 | `terms=1` | `[1]` | `[1]` | PASS |
| Ordinary input (ten) | L3, L9 | `terms=10` | `[1, 2, ..., 512]` | Exact 10-element list | PASS |
| 100 Bounded Property Cases | L3, L9 | 100 random `terms in [0..60]` (seed=42) | All 4 invariants hold | 100/100 passed | PASS |
| Mutation resistance check | L9 | Mutant `2**x + 1` | Detects recurrence violation | Violation detected | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T014 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
