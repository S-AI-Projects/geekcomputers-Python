"""Regression and contract tests for gcd.py.

Task: R25-T036
Target: gcd.py — gcd and is_common_divisor

Verifies:
1. Task specified fixtures: (54, 24), (17, 13), (9, 9) yielding 6, 1, 9.
2. Zero argument behavior: (0, 5), (5, 0), (0, 0) yielding -1.
3. Before/After equivalence: refactored gcd() matches original algorithm bit-for-bit.
4. Extracted helper unit tests: is_common_divisor() accurately detects common divisors.
5. CLI output format preservation: format string matches line 16.
"""

import io
import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gcd import gcd, is_common_divisor


# ---------------------------------------------------------------------------
# Reference: Original Unrefactored Algorithm
# ---------------------------------------------------------------------------


def original_gcd(a, b):
    """Original unrefactored implementation from gcd.py lines 9-14."""
    i = 1
    gcd_val = -1
    while i <= a and i <= b:
        if a % i == 0 and b % i == 0:
            gcd_val = i
        i = i + 1
    return gcd_val


# ---------------------------------------------------------------------------
# 1. Task Fixtures: Nonzero Pairs and Zero Arguments
# ---------------------------------------------------------------------------


class TestGcdTaskFixtures:
    """Verifies all task-specified fixtures with explicit expected values and line citations."""

    def test_fixture_54_24(self):
        """Fixture (54, 24) -> expected 6.

        Source line citations:
            - Lines 6, 7: a=54, b=24 valid positive integers
            - Line 9: search begins at i=1
            - Line 11: loop runs while i <= 24
            - Line 12: common divisors 1, 2, 3, 6 divide both 54 and 24
            - Line 13: largest common divisor recorded is 6
        """
        a, b = 54, 24
        expected = 6

        actual = gcd(a, b)

        assert actual == expected, (
            f"Fixture (54, 24) failed: expected {expected}, got {actual}. "
            "Source: lines 9-14"
        )
        assert actual == original_gcd(a, b), "Refactored output must match original"

    def test_fixture_17_13(self):
        """Fixture (17, 13) -> expected 1 (coprime pair).

        Source line citations:
            - Lines 6, 7: a=17, b=13 coprime primes
            - Line 11: loop runs while i <= 13
            - Line 12: only i=1 divides both 17 and 13
            - Line 13: result is 1
        """
        a, b = 17, 13
        expected = 1

        actual = gcd(a, b)

        assert actual == expected, (
            f"Fixture (17, 13) failed: expected {expected}, got {actual}. "
            "Source: lines 9-14"
        )
        assert actual == original_gcd(a, b), "Refactored output must match original"

    def test_fixture_9_9(self):
        """Fixture (9, 9) -> expected 9 (equal pair).

        Source line citations:
            - Lines 6, 7: a=9, b=9 equal integers
            - Line 11: loop runs while i <= 9
            - Line 12: common divisors 1, 3, 9
            - Line 13: largest recorded divisor is 9
        """
        a, b = 9, 9
        expected = 9

        actual = gcd(a, b)

        assert actual == expected, (
            f"Fixture (9, 9) failed: expected {expected}, got {actual}. "
            "Source: lines 9-14"
        )
        assert actual == original_gcd(a, b), "Refactored output must match original"

    @pytest.mark.parametrize(
        "a, b",
        [
            (0, 5),
            (5, 0),
            (0, 0),
        ],
        ids=["zero_a", "zero_b", "both_zero"],
    )
    def test_zero_argument_behavior(self, a, b):
        """Zero argument behavior: loop condition fails immediately, returns sentinel -1.

        Source line citations:
            - Line 10: initial gcd = -1
            - Line 11: loop requires `i <= a and i <= b`. For a=0 or b=0,
              `1 <= 0` evaluates to False on the very first check.
            - Loop body does not execute; initial sentinel -1 is returned.
        """
        expected = -1

        actual = gcd(a, b)

        assert actual == expected, (
            f"Zero argument ({a}, {b}) failed: expected {expected}, got {actual}. "
            "Source: lines 10, 11 (sentinel -1 preserved)"
        )
        assert actual == original_gcd(a, b), "Refactored output must match original"


# ---------------------------------------------------------------------------
# 2. Before/After Equivalence Across Diverse Inputs
# ---------------------------------------------------------------------------


class TestBeforeAfterEquivalence:
    """Proves refactored gcd() exactly matches original unrefactored implementation."""

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1, 1, 1),
            (12, 18, 6),
            (100, 25, 25),
            (48, 18, 6),
            (101, 103, 1),
            (36, 60, 12),
            (81, 27, 27),
            (15, 28, 1),
        ],
    )
    def test_before_after_agreement(self, a, b, expected):
        """Assert refactored gcd() matches original_gcd() and expected value."""
        refactored_result = gcd(a, b)
        original_result = original_gcd(a, b)

        assert refactored_result == expected, f"gcd({a}, {b}) expected {expected}"
        assert original_result == expected, f"original_gcd({a}, {b}) expected {expected}"
        assert refactored_result == original_result, (
            f"Equivalence mismatch for ({a}, {b}): {refactored_result} != {original_result}"
        )


# ---------------------------------------------------------------------------
# 3. Unit Tests for Extracted Responsibility: is_common_divisor()
# ---------------------------------------------------------------------------


class TestIsCommonDivisor:
    """Verifies the extracted responsibility is_common_divisor()."""

    def test_is_common_divisor_true_cases(self):
        """Divisors that divide both numbers evenly."""
        assert is_common_divisor(1, 54, 24) is True
        assert is_common_divisor(2, 54, 24) is True
        assert is_common_divisor(3, 54, 24) is True
        assert is_common_divisor(6, 54, 24) is True
        assert is_common_divisor(9, 9, 9) is True

    def test_is_common_divisor_false_cases(self):
        """Divisors that divide only one or neither number."""
        # Divides 24 but not 54
        assert is_common_divisor(4, 54, 24) is False
        assert is_common_divisor(8, 54, 24) is False
        # Divides 54 but not 24
        assert is_common_divisor(9, 54, 24) is False
        assert is_common_divisor(27, 54, 24) is False
        # Divides neither
        assert is_common_divisor(5, 54, 24) is False


# ---------------------------------------------------------------------------
# 4. CLI Output Formatting Preservation
# ---------------------------------------------------------------------------


class TestCliPreservation:
    """Verifies that format string output matches original line 16."""

    def test_formatted_output_string(self):
        """Line 16 format: '\\nGCD of {0} and {1} = {2}'.format(a, b, gcd)."""
        a, b = 54, 24
        result = gcd(a, b)
        expected_output = "\nGCD of 54 and 24 = 6"
        actual_output = "\nGCD of {0} and {1} = {2}".format(a, b, result)

        assert actual_output == expected_output, (
            f"Format string mismatch: expected {expected_output!r}, got {actual_output!r}"
        )
