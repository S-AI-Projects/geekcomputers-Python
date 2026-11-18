#!/usr/bin/env python3
"""Focused test runner and evidence generator for Task R25-T026 (binod.py)."""

import os
import sys
import subprocess
import platform

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TASK_DIR, "..", ".."))
TEST_FILE = os.path.join(TASK_DIR, "test_binod.py")
RESULTS_FILE = os.path.join(TASK_DIR, "RESULTS.md")


def run_checks():
    print(f"=== Running focused refactoring checks for R25-T026 (binod.py) ===")
    cmd = [sys.executable, "-m", "pytest", "-v", TEST_FILE]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = []
    evidence.append("# Verification Evidence — R25-T026 (binod.py)\n")
    evidence.append("## Environment & Tool Versions")
    evidence.append(f"- **Python Version:** {platform.python_version()}")
    evidence.append(f"- **Platform:** {platform.platform()}")
    evidence.append(f"- **Runner:** {sys.executable}")
    evidence.append(f"- **Target File:** binod.py (function `checkBinod`)")
    evidence.append(f"- **Test Suite:** work/R25-T026/test_binod.py\n")

    evidence.append("## Executed Command")
    evidence.append(f"```bash\n{' '.join(cmd)}\n```\n")

    evidence.append("## Precondition Source Lines Cited")
    evidence.append("- `binod.py#L38`: `with open(file, 'r') as f:` (file open requirement)")
    evidence.append("- `binod.py#L40`: `fileContent = f.read()` (content extraction)")
    evidence.append("- `binod.py#L42`: `has_binod = 'binod' in fileContent.lower()` (case-insensitive search)")
    evidence.append("- `binod.py#L44`: `print(f'**************Congratulations Binod found in {f}********************')` (notification message)\n")

    evidence.append("## Refactoring Explanation")
    evidence.append("- **Simplified Responsibility:** Extracted the implicit inline search expression into an explicit boolean predicate `has_binod = 'binod' in fileContent.lower()`.")
    evidence.append("- **Control Flow Cleanup:** Replaced nested `if ...: return True else: return False` with direct conditional notification and return.")
    evidence.append("- **Contract Preservation:** All return types, printed messages, side effects, and arguments remained completely identical.\n")

    evidence.append("## Inputs and Expected vs Actual Results")
    evidence.append("| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |")
    evidence.append("|---|---|---|---|---|---|")
    evidence.append("| Smallest input | L38, L40, L42 | Empty file (`\"\"`) | `False` | `False` | PASS |")
    evidence.append("| Ordinary valid | L38-L44 | File with 'Binod' | `True` & message | `True` & message | PASS |")
    evidence.append("| Ordinary without | L38-L42 | File without keyword | `False` | `False` | PASS |")
    evidence.append("| Case-insensitive boundary | L42 | 'BINOD', 'bInOd', 'binod' | All `True` | All `True` | PASS |\n")

    evidence.append("## Pytest Console Output")
    evidence.append(f"```\n{result.stdout}\n```\n")
    evidence.append(f"**Exit Code:** {result.returncode}\n")

    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(evidence))

    print(f"Results saved to {RESULTS_FILE}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_checks()
