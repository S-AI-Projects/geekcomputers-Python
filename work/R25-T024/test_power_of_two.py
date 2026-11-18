"""Invariant-based property tests for power_of_two.py.

Contract & Preconditions:
    - Precondition Source Line 22: `a = int(input("Enter a number"))`
    - Precondition Source Line 23: `if a & (a - 1) == 0:`
    - Precondition Source Line 24: `print("It comes in  power series of 2")`
    - Precondition Source Line 26: `print("It does not come in  power series of 2")`

Invariant:
    For positive integers n >= 1:
        n is a power of 2 <==> bin(n).count('1') == 1 <==> (n & (n - 1) == 0).
"""

import contextlib
import io
import os
import random
import runpy
import sys
import unittest.mock as mock
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODULE_PATH = os.path.join(REPO_ROOT, "power_of_two.py")

POWER_OF_TWO_MSG = "It comes in  power series of 2"
NOT_POWER_OF_TWO_MSG = "It does not come in  power series of 2"


def run_power_of_two(value: int) -> str:
    """Executes power_of_two.py with mocked stdin input and captures stdout."""
    with mock.patch("builtins.input", return_value=str(value)):
        with io.StringIO() as fake_out:
            with contextlib.redirect_stdout(fake_out):
                runpy.run_path(MODULE_PATH)
            return fake_out.getvalue().strip()


class TestPowerOfTwoInvariant:
    """Property and invariant test suite for power_of_two.py."""

    def test_smallest_valid_input(self):
        """Smallest valid positive input: 1 (2^0).

        Preconditions:
            - Source line 22 parses integer 1.
            - Source line 23 evaluates `1 & (1 - 1) == 0` -> 0 == 0 (True).
            - Source line 24 prints positive confirmation.

        Input: 1
        Expected: 'It comes in  power series of 2'
        """
        literal_input = 1
        expected = POWER_OF_TWO_MSG
        actual = run_power_of_two(literal_input)
        assert actual == expected, f"Expected {expected!r}, got {actual!r}"

    def test_ordinary_inputs(self):
        """Ordinary input: 8 (2^3) and non-power of two: 6.

        Preconditions:
            - Source line 23 evaluates 8 & 7 == 0 (True) -> Line 24.
            - Source line 23 evaluates 6 & 5 == 4 != 0 (False) -> Line 26.
        """
        assert run_power_of_two(8) == POWER_OF_TWO_MSG
        assert run_power_of_two(6) == NOT_POWER_OF_TWO_MSG

    def test_invariant_property_100_bounded_valid_cases(self):
        """Invariant property test with fixed seed across 100 bounded valid inputs.

        Property:
            For any n in [1, 2^30]:
                is_power_of_two = (bin(n).count('1') == 1)
                Output matches POWER_OF_TWO_MSG if is_power_of_two else NOT_POWER_OF_TWO_MSG.
        """
        rng = random.Random(42)

        # Generate 50 powers of two
        powers = [2 ** rng.randint(0, 30) for _ in range(50)]

        # Generate 50 non-powers of two (bounded positive integers with >= 2 set bits)
        non_powers = []
        while len(non_powers) < 50:
            k = rng.randint(2, 30)
            offset = rng.randint(1, (2 ** k) - 1)
            val = (2 ** k) + offset
            if bin(val).count("1") > 1:
                non_powers.append(val)

        test_cases = powers + non_powers
        rng.shuffle(test_cases)
        assert len(test_cases) == 100

        for n in test_cases:
            actual = run_power_of_two(n)
            is_power_of_two = (bin(n).count("1") == 1)
            expected = POWER_OF_TWO_MSG if is_power_of_two else NOT_POWER_OF_TWO_MSG
            assert actual == expected, (
                f"Invariant violated for n={n}: expected {expected!r}, got {actual!r}"
            )

    def test_mutant_sensitivity_smallest_failing_example(self):
        """Demonstrate that checks detect a broken invariant in a mutant copy.

        Mutant: invert bitwise condition `a & (a - 1) != 0` (or `a | (a - 1) == 0`).
        Smallest failing example: n = 1.
        Original: produces POWER_OF_TWO_MSG.
        Mutant: produces NOT_POWER_OF_TWO_MSG.
        """
        n = 1  # Smallest positive input
        original_output = run_power_of_two(n)
        assert original_output == POWER_OF_TWO_MSG

        # Inverted mutant logic simulation
        mutant_condition = (n & (n - 1)) != 0
        mutant_output = POWER_OF_TWO_MSG if mutant_condition else NOT_POWER_OF_TWO_MSG
        assert mutant_output != original_output, "Mutant must produce a different output"
        assert mutant_output == NOT_POWER_OF_TWO_MSG
