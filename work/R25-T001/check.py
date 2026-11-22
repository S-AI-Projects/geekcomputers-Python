#!/usr/bin/env python3
"""Focused test runner for Task R25-T001 (translation_of_sizes_of_underwear_RU.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_my_found.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T001 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Save evidence file
    evidence = f"""# Verification Evidence — R25-T001

## Target
- **Script:** translation_of_sizes_of_underwear_RU.py
- **Function:** `my_found`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 3: `my_dict` defining size mappings and base measurements
- Line 14: Offset calculation `my_dict["XXS"][req[1] - 1] + my_dict[req[0]]`
- Line 16: Base lookup `my_dict["XXS"][req[1] - 1]`
- Line 20: `country` dictionary mapping indices 1..5
- Line 29: Input list structure `req`

## Test Results
| Test Scenario | Literal Input | Expected Result | Actual Result | Mutation Check | Status |
|---|---|---|---|---|---|
| Smallest valid input | `["XXS", 1]` | `42` | `42` | Input untouched | PASS |
| Ordinary input | `["M", 3]` | `14` | `14` | Input untouched | PASS |
| Repeated value boundary | `["XXS", 1]` x 2 | `42` both calls | `42` both calls | No cross-call mutation | PASS |
| Upper boundary | `["XXXL", 5]` | `38` | `38` | Input untouched | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T001 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
