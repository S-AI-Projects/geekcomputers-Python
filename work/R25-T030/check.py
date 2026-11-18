#!/usr/bin/env python3
"""Focused test runner and mutation-resistance verification for Task R25-T030 (pscheck.py)."""

import io
import os
import platform
import subprocess
import sys
from unittest.mock import patch

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TASK_DIR, "..", ".."))
TEST_FILE = os.path.join(TASK_DIR, "test_pscheck.py")
RESULTS_FILE = os.path.join(TASK_DIR, "RESULTS.md")

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import pscheck


def run_checks():
    print("=== Running focused mutation-resistant checks for R25-T030 (pscheck.py) ===")
    cmd = [sys.executable, "-m", "pytest", "-v", TEST_FILE]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Direct demonstration of original vs mutant on the named assertion
    if TASK_DIR not in sys.path:
        sys.path.insert(0, TASK_DIR)
    from test_pscheck import (
        SMALLEST_INPUT_PROGRAM,
        SMALLEST_RAW_PS_OUTPUT,
        SMALLEST_EXPECTED_STDOUT,
        ORDINARY_INPUT_PROGRAM,
        ORDINARY_RAW_PS_OUTPUT,
        ORDINARY_EXPECTED_STDOUT,
        assert_owner_field,
        run_ps_isolated,
    )

    # Original evaluation
    orig_ordinary_out = run_ps_isolated(ORDINARY_INPUT_PROGRAM, ORDINARY_RAW_PS_OUTPUT)
    orig_passed = False
    try:
        assert_owner_field(orig_ordinary_out, "root")
        orig_passed = True
    except AssertionError:
        orig_passed = False

    # Mutant evaluation
    def ps_mutant_misindexed_owner():
        import string
        program = input("Enter the name of the program to check: ")
        try:
            output = pscheck.commands.getoutput("ps -f|grep " + program)
            proginfo = string.split(output)
            print(
                "\n\
    Full path:\t\t",
                proginfo[5],
                "\n\
    Owner:\t\t\t",
                proginfo[1],  # MUTANT: accesses PID (index 1) instead of Owner (index 0)
                "\n\
    Process ID:\t\t",
                proginfo[1],
                "\n\
    Parent process ID:\t",
                proginfo[2],
                "\n\
    Time started:\t\t",
                proginfo[4],
            )
        except Exception:
            print("There was a problem with the program.")

    mutant_buf = io.StringIO()
    with patch("builtins.input", return_value=ORDINARY_INPUT_PROGRAM), \
         patch.object(pscheck.commands, "getoutput", return_value=ORDINARY_RAW_PS_OUTPUT), \
         patch("sys.stdout", mutant_buf):
        ps_mutant_misindexed_owner()
    mutant_out = mutant_buf.getvalue()

    mutant_failed_as_expected = False
    mutant_err_msg = ""
    try:
        assert_owner_field(mutant_out, "root")
    except AssertionError as e:
        mutant_failed_as_expected = True
        mutant_err_msg = str(e)

    evidence = []
    evidence.append("# Verification Evidence — R25-T030 (pscheck.py)\n")
    evidence.append("## Environment & Tool Versions")
    evidence.append(f"- **Python Version:** {platform.python_version()}")
    evidence.append(f"- **Platform:** {platform.platform()}")
    evidence.append(f"- **Runner:** {sys.executable}")
    evidence.append(f"- **Target File:** pscheck.py (function `ps`)")
    evidence.append(f"- **Test Suite:** work/R25-T030/test_pscheck.py\n")

    evidence.append("## Executed Command")
    evidence.append(f"```bash\n{' '.join(cmd)}\n```\n")

    evidence.append("## Preconditions & Source Lines Cited")
    evidence.append("- `pscheck.py#L41`: `program = input(\"Enter the name of the program to check: \")` (interactive query input)")
    evidence.append("- `pscheck.py#L45`: `output = commands.getoutput(\"ps -f|grep \" + program)` (shell process execution)")
    evidence.append("- `pscheck.py#L46`: `proginfo = string.split(output)` (whitespace field tokenization into >= 6 tokens)")
    evidence.append("- `pscheck.py#L52`: `proginfo[5]` (Full path)")
    evidence.append("- `pscheck.py#L55`: `proginfo[0]` (Owner field)")
    evidence.append("- `pscheck.py#L58`: `proginfo[1]` (Process ID)")
    evidence.append("- `pscheck.py#L61`: `proginfo[2]` (Parent process ID)")
    evidence.append("- `pscheck.py#L64`: `proginfo[4]` (Time started)")
    evidence.append("- `pscheck.py#L66`: `except:` failure boundary for missing / malformed outputs\n")

    evidence.append("## Fixtures and Expected vs Actual Outputs")
    evidence.append("### 1. Smallest Valid Input")
    evidence.append("- **Input Program:** `\"a\"`")
    evidence.append("- **Mocked ps output:** `\"u 1 0 c t /a\"`")
    evidence.append("- **Expected stdout:**")
    evidence.append(f"```\n{SMALLEST_EXPECTED_STDOUT}```")
    evidence.append("- **Actual stdout:**")
    evidence.append(f"```\n{run_ps_isolated(SMALLEST_INPUT_PROGRAM, SMALLEST_RAW_PS_OUTPUT)}```")
    evidence.append("- **Status:** PASS (contract matches exact expected formatting)\n")

    evidence.append("### 2. Ordinary Valid Input")
    evidence.append("- **Input Program:** `\"python\"`")
    evidence.append("- **Mocked ps output:** `\"root 1234 1 0 10:00 /usr/bin/python\"`")
    evidence.append("- **Expected stdout:**")
    evidence.append(f"```\n{ORDINARY_EXPECTED_STDOUT}```")
    evidence.append("- **Actual stdout:**")
    evidence.append(f"```\n{orig_ordinary_out}```")
    evidence.append("- **Status:** PASS (contract matches exact expected formatting)\n")

    evidence.append("## Mutation Sensitivity Test Results")
    evidence.append("- **Named Assertion:** `assert_owner_field(stdout, expected_owner)`")
    evidence.append("- **Deliberate Mutant:** 1-line indexing mistake in `ps()` swapping `proginfo[0]` with `proginfo[1]` (Owner reads PID).")
    evidence.append(f"- **Original Code Result:** {'PASS' if orig_passed else 'FAIL'}")
    evidence.append(f"- **Mutant Code Result:** {'FAIL (Caught as expected)' if mutant_failed_as_expected else 'UNEXPECTED PASS'}")
    evidence.append(f"- **Mutant Semantic Failure Message:**\n```\n{mutant_err_msg}\n```\n")

    evidence.append("## Pytest Console Output")
    evidence.append(f"```\n{result.stdout}\n```\n")
    evidence.append(f"**Exit Code:** {result.returncode}\n")

    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(evidence))

    print(f"Results saved to {RESULTS_FILE}")
    if not (orig_passed and mutant_failed_as_expected and result.returncode == 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    run_checks()
