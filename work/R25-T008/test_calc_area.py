"""Focused regression tests for failure branch and ordinary calculations in calc_area.py.

Precondition citations:
    - Source Line 5: `shape = int(...)` choice input
    - Source Line 11: `shape == 1` square area formula
    - Source Line 14: `shape == 2` rectangle area formula
    - Source Line 32: `else: print("You have selected wrong choice.")` failure fallback branch
    - Source Line 35: `restart = input(...)` continuation prompt
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import calc_area


def run_main_with_inputs(inputs):
    """Helper to simulate console input and capture printed messages."""
    input_queue = list(inputs)
    outputs = []

    def mock_input(prompt=""):
        if not input_queue:
            raise EOFError("No more mock inputs")
        return input_queue.pop(0)

    def mock_print(*args, **kwargs):
        outputs.append(" ".join(str(a) for a in args))

    calc_area.main(input_fn=mock_input, print_fn=mock_print)
    return outputs


class TestCalcAreaFailureAndContracts:
    """Verifies failure branch coverage, valid input behavior, and state preservation."""

    def test_documented_failure_branch_wrong_choice(self):
        """Exercises documented failure branch at line 32 when choice is out-of-bounds.

        Preconditions:
            - Source line 5: shape integer parsed from user input.
            - Source line 32: else branch triggered when shape not in 1..7.
        Literal input:
            shape = '9', restart = 'n'
        Independently calculated expected output:
            "You have selected wrong choice."
        """
        outputs = run_main_with_inputs(["9", "n"])
        assert any("You have selected wrong choice." in line for line in outputs), (
            f"Expected failure message not found in outputs: {outputs}"
        )

    def test_smallest_valid_input_zero_side_square(self):
        """Smallest valid input: square with side = 0.0.

        Preconditions:
            - Source line 11: side**2
        Literal input:
            shape = '1', side = '0.0', restart = 'n'
        Independently calculated expected output:
            "Area of square = 0.0"
        """
        outputs = run_main_with_inputs(["1", "0.0", "n"])
        assert any("Area of square = 0.0" in line for line in outputs), (
            f"Expected 'Area of square = 0.0' in {outputs}"
        )

    def test_ordinary_valid_input(self):
        """Ordinary input: square with side = 5.0.

        Preconditions:
            - Source line 11: 5.0**2 = 25.0
        Literal input:
            shape = '1', side = '5.0', restart = 'n'
        Independently calculated expected output:
            "Area of square = 25.0"
        """
        outputs = run_main_with_inputs(["1", "5.0", "n"])
        assert any("Area of square = 25.0" in line for line in outputs)

    def test_ordinary_call_succeeds_after_failure_case(self):
        """Ensures that executing a failure branch does not corrupt state or block subsequent valid calls."""
        # First: trigger failure case
        fail_outputs = run_main_with_inputs(["99", "n"])
        assert any("You have selected wrong choice." in line for line in fail_outputs)

        # Immediately after: run ordinary valid calculation (rectangle 4 x 5)
        success_outputs = run_main_with_inputs(["2", "4.0", "5.0", "n"])
        assert any("Area of rectangle = 20.0" in line for line in success_outputs)
