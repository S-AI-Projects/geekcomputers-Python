"""Focused regression tests for recursive-fibonacci.py (fib function).

Task: R25-T031
Target: recursive-fibonacci.py -> fib(n)
Stated fixture: indices 0, 1, 2, 5, 10 -> values 0, 1, 1, 5, 55
"""

import importlib.util
from pathlib import Path
from unittest.mock import patch

try:
    import pytest
    parametrize = pytest.mark.parametrize
except ImportError:
    pytest = None
    def parametrize(*args, **kwargs):
        def decorator(fn):
            return fn
        return decorator

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "recursive-fibonacci.py"

# Dynamic import to handle hyphenated file name
spec = importlib.util.spec_from_file_location("recursive_fibonacci", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fib = module.fib


# ---------------------------------------------------------------------------
# Fixture Value & Domain Boundary Tests
# ---------------------------------------------------------------------------

def test_fib_smallest_supported_input_zero():
    """Test index 0: Smallest supported input (base case root).
    0-based indexing convention yields 0.
    """
    n = 0
    expected = 0
    actual = fib(n)
    assert actual == expected, f"Input: {n}, expected: {expected}, actual: {actual}"


def test_fib_base_case_boundary_one():
    """Test index 1: Second base case boundary.
    0-based indexing convention yields 1.
    """
    n = 1
    expected = 1
    actual = fib(n)
    assert actual == expected, f"Input: {n}, expected: {expected}, actual: {actual}"


def test_fib_repeated_value_boundary_two():
    """Test index 2: First recursive step and repeated-value boundary.
    fib(2) = fib(1) + fib(0) = 1 + 0 = 1 (repeated value with fib(1)).
    """
    n = 2
    expected = 1
    actual = fib(n)
    assert actual == expected, f"Input: {n}, expected: {expected}, actual: {actual}"
    assert actual == fib(1), "fib(2) must equal fib(1) representing repeated value boundary"


def test_fib_ordinary_input_five():
    """Test index 5: Ordinary input in the middle domain.
    fib(5) = 5.
    """
    n = 5
    expected = 5
    actual = fib(n)
    assert actual == expected, f"Input: {n}, expected: {expected}, actual: {actual}"


def test_fib_larger_ordinary_input_ten():
    """Test index 10: Larger ordinary input with multi-level recursive expansion.
    fib(10) = 55.
    """
    n = 10
    expected = 55
    actual = fib(n)
    assert actual == expected, f"Input: {n}, expected: {expected}, actual: {actual}"


@parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (5, 5),
        (10, 55),
    ],
)
def test_fib_stated_fixture_all(n, expected):
    """Parametrized verification of the entire stated fixture:
    indices 0, 1, 2, 5, 10 yielding 0, 1, 1, 5, 55.
    """
    actual = fib(n)
    assert actual == expected, f"Fixture index {n}: expected {expected}, got {actual}"


# ---------------------------------------------------------------------------
# Mutation & Purity Tests
# ---------------------------------------------------------------------------

def test_fib_no_observable_mutation():
    """Verify that calling fib(n) produces no observable mutation on inputs,
    caller state, or module globals.
    """
    globals_before = dict(module.__dict__)
    input_value = 5
    result = fib(input_value)

    assert result == 5
    assert input_value == 5, "Input integer was mutated"
    # Ensure module attributes did not leak new mutable state
    assert set(globals_before.keys()) == set(module.__dict__.keys()), "Module globals mutated"


def test_fib_idempotency_and_pure_function():
    """Verify repeated execution of fib(n) produces consistent results without side effects."""
    first_run = [fib(i) for i in (0, 1, 2, 5, 10)]
    second_run = [fib(i) for i in (0, 1, 2, 5, 10)]
    assert first_run == second_run == [0, 1, 1, 5, 55], "fib is not idempotent across multiple runs"


# ---------------------------------------------------------------------------
# External Dependencies & Mocked I/O Tests
# ---------------------------------------------------------------------------

def test_fib_external_io_mocked():
    """Verify that fib executes without performing any external I/O (files, network, stdout)."""
    with patch("builtins.print") as mock_print, \
         patch("builtins.open") as mock_open:
        result = fib(5)
        assert result == 5
        mock_print.assert_not_called()
        mock_open.assert_not_called()


# ---------------------------------------------------------------------------
# Public Interface & Contract Validation
# ---------------------------------------------------------------------------

def test_fib_public_interface_and_contract():
    """Verify public interface, callable status, return types, and docstring contract."""
    import inspect

    assert callable(fib), "fib must be callable"
    sig = inspect.signature(fib)
    assert "n" in sig.parameters, "fib parameter signature must accept 'n'"
    assert len(sig.parameters) == 1, "fib must take exactly 1 parameter"

    doc = inspect.getdoc(fib)
    assert doc is not None, "fib must contain a contract docstring"
    assert "Fibonacci" in doc or "fib" in doc.lower()
    assert isinstance(fib(0), int), "fib must return an int"


if __name__ == "__main__":
    import sys
    test_functions = [
        test_fib_smallest_supported_input_zero,
        test_fib_base_case_boundary_one,
        test_fib_repeated_value_boundary_two,
        test_fib_ordinary_input_five,
        test_fib_larger_ordinary_input_ten,
        test_fib_no_observable_mutation,
        test_fib_idempotency_and_pure_function,
        test_fib_external_io_mocked,
        test_fib_public_interface_and_contract,
    ]
    passed = 0
    failed = 0
    print(f"Running {len(test_functions) + 5} regression tests for recursive-fibonacci.py...")
    for fn in test_functions:
        try:
            fn()
            print(f"  PASS: {fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL: {fn.__name__}: {e}")
            failed += 1

    # Also run the fixture parametrized cases directly
    for n, expected in [(0, 0), (1, 1), (2, 1), (5, 5), (10, 55)]:
        try:
            test_fib_stated_fixture_all(n, expected)
            print(f"  PASS: test_fib_stated_fixture_all[{n}->{expected}]")
            passed += 1
        except Exception as e:
            print(f"  FAIL: test_fib_stated_fixture_all[{n}->{expected}]: {e}")
            failed += 1

    print(f"\nTotal: {passed} passed, {failed} failed.")
    sys.exit(1 if failed > 0 else 0)
