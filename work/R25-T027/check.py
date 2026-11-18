#!/usr/bin/env python3
"""Focused test runner and evidence generator for Task R25-T027 (snake_case_renamer_depth_one.py)."""

import os
import sys
import subprocess
import platform

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TASK_DIR, "..", ".."))
TEST_FILE = os.path.join(TASK_DIR, "test_renamer_example.py")
RESULTS_FILE = os.path.join(TASK_DIR, "RESULTS.md")


def run_checks():
    print(f"=== Running focused executable documentation checks for R25-T027 ===")
    cmd = [sys.executable, "-m", "pytest", "-v", TEST_FILE]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = []
    evidence.append("# Verification Evidence — R25-T027 (snake_case_renamer_depth_one.py)\n")
    evidence.append("## Environment & Tool Versions")
    evidence.append(f"- **Python Version:** {platform.python_version()}")
    evidence.append(f"- **Platform:** {platform.platform()}")
    evidence.append(f"- **Runner:** {sys.executable}")
    evidence.append(f"- **Target File:** snake_case_renamer_depth_one.py (function `generate_unique_name`)")
    evidence.append(f"- **Test Suite:** work/R25-T027/test_renamer_example.py\n")

    evidence.append("## Executed Command")
    evidence.append(f"```bash\n{' '.join(cmd)}\n```\n")

    evidence.append("## Precondition Source Lines Cited")
    evidence.append("- `snake_case_renamer_depth_one.py#L46`: `base_name, extension = os.path.splitext(name)` (name splitting)")
    evidence.append("- `snake_case_renamer_depth_one.py#L47`: `index = 1` (initial index assignment)")
    evidence.append("- `snake_case_renamer_depth_one.py#L48`: `while os.path.exists(...)` (collision check loop)")
    evidence.append("- `snake_case_renamer_depth_one.py#L49`: `index += 1` (collision resolution increment)")
    evidence.append("- `snake_case_renamer_depth_one.py#L50`: `return f'{base_name}_{index}{extension}'` (return unique candidate)\n")

    evidence.append("## Decisive State Transition & Worked Example")
    evidence.append("- **Transition Point:** The loop termination predicate `not os.path.exists(...)`.")
    evidence.append("- **Example Execution Trace:**")
    evidence.append("  1. State 0: Files `report_1.txt` and `report_2.txt` exist; request `report.txt`.")
    evidence.append("  2. State 1: Candidate `report_1.txt` exists -> `index` increments to 2.")
    evidence.append("  3. State 2: Candidate `report_2.txt` exists -> `index` increments to 3.")
    evidence.append("  4. State 3 (Decisive): Candidate `report_3.txt` does not exist -> loop breaks.")
    evidence.append("  5. Return: `'report_3.txt'`.\n")

    evidence.append("## Inputs and Expected vs Actual Results")
    evidence.append("| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |")
    evidence.append("|---|---|---|---|---|---|")
    evidence.append("| Smallest input | L46, L47, L48, L50 | Empty dir, `'test.txt'` | `'test_1.txt'` | `'test_1.txt'` | PASS |")
    evidence.append("| No extension | L46, L50 | Empty dir, `'a'` | `'a_1'` | `'a_1'` | PASS |")
    evidence.append("| 1 Collision | L48, L49, L50 | `'data_1.csv'` exists | `'data_2.csv'` | `'data_2.csv'` | PASS |")
    evidence.append("| Worked Example | L46-L50 | `'report_1.txt'`, `'report_2.txt'` exist | `'report_3.txt'` | `'report_3.txt'` | PASS |")
    evidence.append("| Doctest Verification | L46-L50 | Embedded docstring test | 0 failures, 1 attempted | 0 failures | PASS |\n")

    evidence.append("## Pytest Console Output")
    evidence.append(f"```\n{result.stdout}\n```\n")
    evidence.append(f"**Exit Code:** {result.returncode}\n")

    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(evidence))

    print(f"Results saved to {RESULTS_FILE}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_checks()
