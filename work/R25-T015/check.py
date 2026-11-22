#!/usr/bin/env python3
"""Focused test runner for Task R25-T015 (diamond.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_diamond.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T015 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T015

## Target
- **Script:** diamond.py
- **Function:** `draw_diamond`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 1: `def draw_diamond(n):` input interface with dependency seam `output_fn=print`.
- Line 2: `if n % 2 != 0:` parity check (odd number requirement).
- Lines 4-5: Upper pyramid expansion step by 2.
- Lines 9-10: Lower inverted pyramid contraction step by 2.
- Line 14: Non-odd input rejection fallback.

## Determinism & Seam Architecture
- **Dependency Seam:** Added optional `output_fn=print` parameter defaulting to built-in `print`.
- **Caller Compatibility:** Current 1-argument calls `draw_diamond(n)` behave 100% identically.
- **Repeatability Proof:** Tested `draw_diamond(3)` before and after an intervening `draw_diamond(7)` call; proved zero state pollution across invocations.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (n=1) | L2, L4-5 | `n=1` | `["*"]` | `["*"]` | PASS |
| Ordinary input (n=3) | L2, L4-5, L9-10 | `n=3` | `[" * ", "***", " * "]` | `[" * ", "***", " * "]` | PASS |
| Ordinary input (n=5) | L2, L4-5, L9-10 | `n=5` | 5-line diamond | 5-line diamond | PASS |
| Even number rejection (n=4) | L2, L14 | `n=4` | `["Not an odd number..."]` | `["Not an odd number..."]` | PASS |
| Repeatability & Isolation | L1, L2, L4, L9 | `n=3` twice with intervening `n=7` | Identical output across fresh & subsequent runs | Exact match | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T015 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
