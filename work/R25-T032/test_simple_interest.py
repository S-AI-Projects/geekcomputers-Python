"""Boundary tests for simpleInterest() from simpleInterest.py.

Task: R25-T032
Target: simpleInterest.py — simpleInterest function

Each test uses literal inputs with independently calculated expected outputs.
Every assertion cites the source line establishing the precondition.
"""

import sys
import os

# Ensure the repo root is on sys.path so we can import simpleInterest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from simpleInterest import simpleInterest


# ---------------------------------------------------------------------------
# Valid Interior — Ordinary Input
# ---------------------------------------------------------------------------


def test_simple_interest_ordinary_input():
    """Ordinary interior input.

    Inputs: principle=1000.0, time=2, rate=5.0
    Expected: (1000.0 * 2 * 5.0) / 100 = 100.0
    Source lines: Line 1 (principle float), Line 2 (time int),
                  Line 3 (rate float), Line 4 (formula).
    """
    # Precondition: Line 1 — principle accepted as float
    # Precondition: Line 2 — time accepted as int
    # Precondition: Line 3 — rate accepted as float
    # Precondition: Line 4 — formula (principle * time * rate) / 100
    result = simpleInterest(1000.0, 2, 5.0)
    assert result == 100.0, (
        f"Expected 100.0 for ordinary input, got {result}. "
        "Source: Line 4 formula (1000.0 * 2 * 5.0) / 100"
    )


# ---------------------------------------------------------------------------
# Valid Boundary — Smallest Valid Input (all zeros)
# ---------------------------------------------------------------------------


def test_simple_interest_smallest_valid_input_zero():
    """Smallest valid input — zero boundary for all parameters.

    Inputs: principle=0.0, time=0, rate=0.0
    Expected: (0.0 * 0 * 0.0) / 100 = 0.0
    Source lines: Line 1 (0.0 is valid float), Line 2 (0 is valid int),
                  Line 3 (0.0 is valid float), Line 4 (formula).
    """
    # Precondition: Line 1 — principle=0.0 is the smallest valid float value
    # Precondition: Line 2 — time=0 is the smallest valid int value
    # Precondition: Line 3 — rate=0.0 is the smallest valid float value
    # Precondition: Line 4 — formula (0.0 * 0 * 0.0) / 100 = 0.0
    result = simpleInterest(0.0, 0, 0.0)
    assert result == 0.0, (
        f"Expected 0.0 for smallest valid input (all zeros), got {result}. "
        "Source: Line 4 formula (0.0 * 0 * 0.0) / 100"
    )


# ---------------------------------------------------------------------------
# Valid Boundary — Smallest Positive Non-Zero Input
# ---------------------------------------------------------------------------


def test_simple_interest_smallest_positive_input():
    """Smallest positive non-zero input for each parameter.

    Inputs: principle=1.0, time=1, rate=1.0
    Expected: (1.0 * 1 * 1.0) / 100 = 0.01
    Source lines: Line 1 (1.0 float), Line 2 (1 int),
                  Line 3 (1.0 float), Line 4 (formula).
    """
    # Precondition: Line 1 — principle=1.0 smallest positive float unit
    # Precondition: Line 2 — time=1 smallest positive int unit
    # Precondition: Line 3 — rate=1.0 smallest positive float unit
    # Precondition: Line 4 — formula (1.0 * 1 * 1.0) / 100 = 0.01
    result = simpleInterest(1.0, 1, 1.0)
    assert result == 0.01, (
        f"Expected 0.01 for smallest positive input, got {result}. "
        "Source: Line 4 formula (1.0 * 1 * 1.0) / 100"
    )


# ---------------------------------------------------------------------------
# Valid Boundary — Zero Principle (one parameter at boundary)
# ---------------------------------------------------------------------------


def test_simple_interest_zero_principle_boundary():
    """Boundary: principle is zero while other inputs are ordinary.

    Inputs: principle=0.0, time=2, rate=5.0
    Expected: (0.0 * 2 * 5.0) / 100 = 0.0
    Source: Line 1 (principle=0.0 valid), Line 4 (formula).
    """
    # Precondition: Line 1 — principle=0.0 is valid boundary value
    # Precondition: Line 4 — formula (0.0 * 2 * 5.0) / 100 = 0.0
    result = simpleInterest(0.0, 2, 5.0)
    assert result == 0.0, (
        f"Expected 0.0 for zero principle, got {result}. "
        "Source: Line 4 formula (0.0 * 2 * 5.0) / 100"
    )


# ---------------------------------------------------------------------------
# Valid Boundary — Zero Time (one parameter at boundary)
# ---------------------------------------------------------------------------


def test_simple_interest_zero_time_boundary():
    """Boundary: time is zero while other inputs are ordinary.

    Inputs: principle=1000.0, time=0, rate=5.0
    Expected: (1000.0 * 0 * 5.0) / 100 = 0.0
    Source: Line 2 (time=0 valid), Line 4 (formula).
    """
    # Precondition: Line 2 — time=0 is valid boundary value
    # Precondition: Line 4 — formula (1000.0 * 0 * 5.0) / 100 = 0.0
    result = simpleInterest(1000.0, 0, 5.0)
    assert result == 0.0, (
        f"Expected 0.0 for zero time, got {result}. "
        "Source: Line 4 formula (1000.0 * 0 * 5.0) / 100"
    )


# ---------------------------------------------------------------------------
# Valid Boundary — Zero Rate (one parameter at boundary)
# ---------------------------------------------------------------------------


def test_simple_interest_zero_rate_boundary():
    """Boundary: rate is zero while other inputs are ordinary.

    Inputs: principle=1000.0, time=2, rate=0.0
    Expected: (1000.0 * 2 * 0.0) / 100 = 0.0
    Source: Line 3 (rate=0.0 valid), Line 4 (formula).
    """
    # Precondition: Line 3 — rate=0.0 is valid boundary value
    # Precondition: Line 4 — formula (1000.0 * 2 * 0.0) / 100 = 0.0
    result = simpleInterest(1000.0, 2, 0.0)
    assert result == 0.0, (
        f"Expected 0.0 for zero rate, got {result}. "
        "Source: Line 4 formula (1000.0 * 2 * 0.0) / 100"
    )


# ---------------------------------------------------------------------------
# Explicitly Unsupported — Non-numeric type (TypeError)
# ---------------------------------------------------------------------------


def test_simple_interest_unsupported_non_numeric_type():
    """Unsupported: passing None raises TypeError per Python multiplication.

    The source does not define rejection for non-numeric types; Python's
    standard multiplication on NoneType raises TypeError naturally.
    Source: Line 4 — multiplication fails on incompatible types.
    """
    import pytest

    # Precondition: Line 4 — multiplication with None raises TypeError
    with pytest.raises(TypeError):
        simpleInterest(None, 2, 5.0)
