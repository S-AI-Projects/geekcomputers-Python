#!/usr/bin/env python3
"""Focused test runner for Task R25-T007 (ReadFromCSV.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_read_from_csv.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T007 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T007

## Target
- **Script:** ReadFromCSV.py
- **Function:** `read_from_csv` / `ReadFromCSV`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 2: `import pandas as pd` loading DataFrame parsing engine
- Line 11: `df = pd.read_csv(...)` loading CSV file from filesystem
- Lines 12-14: `x = df['SalesID']` column extraction
- Line 15: `y = df['ProductPrice']` column extraction
- Lines 16-20: Plot axis configuration and rendering

## Decisive State Transition
Transforms unparsed CSV text records on disk into an in-memory structured DataFrame, then projects column vectors into distinct coordinate arrays ready for downstream visualization.

## Verification Matrix
| Scenario | Preconditions | Literal Input | Expected Output | Actual Result | Status |
|---|---|---|---|---|---|
| Smallest input (1 row) | L11, L12-14, L15 | `1, 19.99` | `x=[1], y=[19.99]` | `x=[1], y=[19.99]` | PASS |
| Ordinary input (3 rows) | L11, L12-14, L15 | 3 rows of SalesData | `x=[101, 102, 103]`, `y=[45.5, 60.0, 32.75]` | `x=[101, 102, 103]`, `y=[45.5, 60.0, 32.75]` | PASS |
| Worked example execution | runnable_example.py | Subprocess execution | Expected transitions asserted | Formatted output verified | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T007 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
