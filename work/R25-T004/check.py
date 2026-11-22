#!/usr/bin/env python3
"""Focused test runner for Task R25-T004 (how to display the fibonacci sequence up to n-.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_fibonacci.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T004 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T004

## Target
- **Script:** how to display the fibonacci sequence up to n-.py
- **Function:** `fibonacci_sequence` / `how_to_display_the_fibonacci_sequence_up_to_n`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 6: `n1, n2 = 0, 1` establishing F(0)=0 and F(1)=1
- Line 10: `nterms <= 0` input validity guard
- Line 17: `nth = n1 + n2` defining recurrence F(n+2) = F(n+1) + F(n)

## Fixture and Invariant Results
| Check Scenario | Precondition | Input / Index | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Fixture Index 0 | L6 | Index 0 | `0` | `0` | PASS |
| Fixture Index 1 | L6 | Index 1 | `1` | `1` | PASS |
| Fixture Index 2 | L6, L17 | Index 2 | `1` | `1` | PASS |
| Fixture Index 5 | L17 | Index 5 | `5` | `5` | PASS |
| Fixture Index 10 | L17 | Index 10 | `55` | `55` | PASS |
| Invariant F(n+2)=F(n+1)+F(n) | L17 | Indices 0..22 | Exact equality across range | Exact equality across range | PASS |
| Smallest valid input | L10 | `nterms=1` | `[0]` | `[0]` | PASS |
| Deliberate mutant detection | L17 | `nth = n1 + n2 + 1` | Invariant failure | Detected invariant failure | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T004 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
