"""Mutation-resistant regression tests for pscheck.py (ps).

Task: R25-T030
Target: pscheck.py -> ps()

Source Lines Establishing Preconditions:
  - Line 41: `program = input("Enter the name of the program to check: ")`
    Precondition: user provides program search term string via interactive stdin.
  - Line 45: `output = commands.getoutput("ps -f|grep " + program)`
    Precondition: shell execution returns space-delimited standard ps output string.
  - Line 46: `proginfo = string.split(output)`
    Precondition: whitespace tokenization splits output into field list of >= 6 elements.
  - Lines 49-65: formatted stdout print:
    Line 52: `proginfo[5]` (Full path)
    Line 55: `proginfo[0]` (Owner)
    Line 58: `proginfo[1]` (Process ID)
    Line 61: `proginfo[2]` (Parent process ID)
    Line 64: `proginfo[4]` (Time started)
  - Line 66: `except:`
    Precondition: any exception (e.g. IndexError on < 6 tokens) prints failure notice.
"""

import io
import os
import sys
from unittest.mock import patch
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import pscheck


# ---------------------------------------------------------------------------
# Fixture definitions & literal expected outputs
# ---------------------------------------------------------------------------

# Smallest valid input:
# Literal input program: "a"
# Minimal valid token line (indices 0..5): "u 1 0 c t /a"
# Precondition lines: pscheck.py#L41, L45, L46, L49-65
SMALLEST_INPUT_PROGRAM = "a"
SMALLEST_RAW_PS_OUTPUT = "u 1 0 c t /a"
SMALLEST_EXPECTED_STDOUT = (
    "\n    Full path:\t\t /a \n"
    "    Owner:\t\t\t u \n"
    "    Process ID:\t\t 1 \n"
    "    Parent process ID:\t 0 \n"
    "    Time started:\t\t t\n"
)

# Ordinary input:
# Literal input program: "python"
# Standard ps output: "root 1234 1 0 10:00 /usr/bin/python"
# Precondition lines: pscheck.py#L41, L45, L46, L49-65
ORDINARY_INPUT_PROGRAM = "python"
ORDINARY_RAW_PS_OUTPUT = "root 1234 1 0 10:00 /usr/bin/python"
ORDINARY_EXPECTED_STDOUT = (
    "\n    Full path:\t\t /usr/bin/python \n"
    "    Owner:\t\t\t root \n"
    "    Process ID:\t\t 1234 \n"
    "    Parent process ID:\t 1 \n"
    "    Time started:\t\t 10:00\n"
)

FAILURE_EXPECTED_STDOUT = "There was a problem with the program.\n"


# ---------------------------------------------------------------------------
# Named assertions
# ---------------------------------------------------------------------------

def assert_owner_field(stdout_text: str, expected_owner: str) -> None:
    """Named assertion verifying semantic correctness of Owner field formatting."""
    expected_line = f"Owner:\t\t\t {expected_owner}"
    assert expected_line in stdout_text, (
        f"Semantic regression detected: expected {expected_line!r} in stdout, got:\n{stdout_text}"
    )


def assert_full_formatted_contract(stdout_text: str, expected_stdout: str) -> None:
    """Named assertion verifying exact output contract formatting."""
    assert stdout_text == expected_stdout, (
        f"Output contract mismatch:\nExpected:\n{expected_stdout!r}\nActual:\n{stdout_text!r}"
    )


# ---------------------------------------------------------------------------
# Helper runner
# ---------------------------------------------------------------------------

def run_ps_isolated(program_input: str, ps_raw_output: str) -> str:
    """Run pscheck.ps() with isolated stdin, stdout, and commands.getoutput."""
    buf = io.StringIO()
    with patch("builtins.input", return_value=program_input), \
         patch.object(pscheck.commands, "getoutput", return_value=ps_raw_output), \
         patch("sys.stdout", buf):
        pscheck.ps()
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_smallest_valid_input():
    """Verify ps() output on smallest valid input.

    Precondition source lines:
      - Line 41: input() -> 'a'
      - Line 45: commands.getoutput() -> 'u 1 0 c t /a'
      - Line 46: string.split() -> 6 tokens
      - Lines 49-65: print() formatted output
    """
    actual_stdout = run_ps_isolated(SMALLEST_INPUT_PROGRAM, SMALLEST_RAW_PS_OUTPUT)
    assert_owner_field(actual_stdout, "u")
    assert_full_formatted_contract(actual_stdout, SMALLEST_EXPECTED_STDOUT)


def test_ordinary_valid_input():
    """Verify ps() output on ordinary valid input.

    Precondition source lines:
      - Line 41: input() -> 'python'
      - Line 45: commands.getoutput() -> 'root 1234 1 0 10:00 /usr/bin/python'
      - Line 46: string.split() -> 6 tokens
      - Lines 49-65: print() formatted output
    """
    actual_stdout = run_ps_isolated(ORDINARY_INPUT_PROGRAM, ORDINARY_RAW_PS_OUTPUT)
    assert_owner_field(actual_stdout, "root")
    assert_full_formatted_contract(actual_stdout, ORDINARY_EXPECTED_STDOUT)


def test_mutation_detection_owner_field_swap():
    """Prove that assert_owner_field detects a plausible 1-line indexing mistake.

    Original: pscheck.py#L55 accesses proginfo[0] (Owner: root).
    Mutant: alters line 55 to access proginfo[1] (Owner: 1234).

    Requirement:
      - Original passes assert_owner_field.
      - Mutant fails the same named assertion for semantic reason.
    """
    # 1. Original execution must pass
    original_stdout = run_ps_isolated(ORDINARY_INPUT_PROGRAM, ORDINARY_RAW_PS_OUTPUT)
    assert_owner_field(original_stdout, "root")

    # 2. Define deliberate mutant: 1-line indexing mistake (proginfo[1] instead of proginfo[0])
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

    # 3. Mutant execution
    mutant_buf = io.StringIO()
    with patch("builtins.input", return_value=ORDINARY_INPUT_PROGRAM), \
         patch.object(pscheck.commands, "getoutput", return_value=ORDINARY_RAW_PS_OUTPUT), \
         patch("sys.stdout", mutant_buf):
        ps_mutant_misindexed_owner()
    mutant_stdout = mutant_buf.getvalue()

    # 4. Mutant must fail the same named assertion
    with pytest.raises(AssertionError) as exc_info:
        assert_owner_field(mutant_stdout, "root")

    assert "Semantic regression detected" in str(exc_info.value)
    assert "expected 'Owner:\\t\\t\\t root'" in str(exc_info.value)


def test_failure_behavior_empty_or_malformed_output():
    """Verify error boundary behavior when process output is empty or < 6 tokens.

    Precondition source lines:
      - Line 45: commands.getoutput() returns empty string ""
      - Line 46: string.split() yields []
      - Line 52: proginfo[5] raises IndexError
      - Line 66: except handler catches and prints 'There was a problem with the program.'
    """
    actual_stdout = run_ps_isolated("nonexistent_service_xyz", "")
    assert actual_stdout == FAILURE_EXPECTED_STDOUT


def test_input_isolation_and_idempotency():
    """Verify that multiple invocations with fresh equivalent inputs are idempotent."""
    out1 = run_ps_isolated(ORDINARY_INPUT_PROGRAM, ORDINARY_RAW_PS_OUTPUT)
    out2 = run_ps_isolated(ORDINARY_INPUT_PROGRAM, ORDINARY_RAW_PS_OUTPUT)
    assert out1 == out2 == ORDINARY_EXPECTED_STDOUT
