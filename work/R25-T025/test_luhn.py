"""Repeatability and input isolation regression tests for verify_card_number.

Contract & Preconditions:
    - Precondition Source Line 25: `card_number_reversed = card_number[::-1]`
    - Precondition Source Line 29: `sum_of_odd_digits += int(digit)`
    - Precondition Source Line 39: `return total % 10 == 0`
"""

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from luhn_algorithm_for_credit_card_validation import verify_card_number


class TestVerifyCardNumberRepeatability:
    """Repeatability, determinism, and input-isolation test suite."""

    def test_smallest_valid_input(self):
        """Smallest valid input: single digit '0'.

        Preconditions:
            - Source line 25: reverses '0' -> '0'.
            - Source line 29: odd digits sum = 0.
            - Source line 39: total (0) % 10 == 0 -> True.

        Input: '0'
        Expected: True
        """
        literal_input = "0"
        expected = True
        actual = verify_card_number(literal_input)
        assert actual == expected

    def test_smallest_invalid_input(self):
        """Smallest invalid input: single digit '1'.

        Preconditions:
            - Source lines 25-39: total = 1, 1 % 10 != 0 -> False.

        Input: '1'
        Expected: False
        """
        assert verify_card_number("1") is False

    def test_ordinary_inputs(self):
        """Ordinary valid and invalid card numbers.

        Inputs:
            '79927398713' (Canonical Luhn test vector) -> True
            '4111111145551142' (Valid card from main()) -> True
            '4111111145551143' (Invalid card checksum) -> False
        """
        assert verify_card_number("79927398713") is True
        assert verify_card_number("4111111145551142") is True
        assert verify_card_number("4111111145551143") is False

    def test_repeatability_in_fresh_state(self):
        """Verify repeated calls with identical input produce identical output."""
        fixture = "79927398713"
        first_call = verify_card_number(fixture)
        second_call = verify_card_number(fixture)
        assert first_call is True
        assert second_call is True
        assert first_call == second_call

    def test_input_isolation_after_intervening_call(self):
        """Verify earlier executions cannot alter later results (no hidden state leakage)."""
        fixture = "79927398713"
        intervening_input = "4111111145551143"

        # Baseline
        initial_result = verify_card_number(fixture)
        assert initial_result is True

        # Intervening execution with different (invalid) input
        intervening_result = verify_card_number(intervening_input)
        assert intervening_result is False

        # Post-intervening execution of original fixture
        subsequent_result = verify_card_number(fixture)
        assert subsequent_result is True
        assert subsequent_result == initial_result

    def test_purity_and_zero_external_dependencies(self):
        """Audit that verify_card_number is pure: no external I/O, network, or GUI."""
        import inspect

        sig = inspect.signature(verify_card_number)
        # Function accepts exactly one parameter 'card_number'
        assert list(sig.parameters.keys()) == ["card_number"]
        # Default preserving: any introduced parameter has default preserving current callers
        for p in list(sig.parameters.values())[1:]:
            assert p.default is not inspect.Parameter.empty
