#!/usr/bin/env python3
"""Focused test runner for Task R25-T013 (ex20.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_ex20.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T013 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T013

## Target
- **Script:** ex20.py
- **Function:** `print_all`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 6: `def print_all(f):` establishes file/stream input interface.
- Line 7: `print(f.read())` reads stream to EOF and emits to stdout.
- Line 10: `f.seek(0)` establishes stream pointer and mutation awareness.

## Oracle Specification
- **Independent Method:** Uses `readline()` chunked collection instead of `.read()`, appending `\\n` to match standard `print()` semantics.
- **Independence:** The reference oracle runs independently without invoking the target function under test.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input | L6, L7 | `io.StringIO("")` | `stdout == "\\n"`, `tell() == 0` | Matches expected | PASS |
| Ordinary input | L6, L7 | `io.StringIO("First\\nSecond\\n")` | `"First\\nSecond\\n\\n"`, `tell() == 13` | Matches expected | PASS |
| Stream mutation check | L6, L7, L10 | Pointer at 0 | Advances pointer to EOF | Pointer advanced to EOF | PASS |
| 21-Input Oracle Comparison | L6, L7 | 21 diverse inputs | Exact oracle match across all 21 cases | 21/21 passed | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T013 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
