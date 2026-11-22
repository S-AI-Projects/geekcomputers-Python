"""Executable documentation and regression tests for add() in simple_calculator.py.

Task: R25-T037
Target: simple_calculator.py — add (line 18)

Verifies:
1. Embedded doctests in module and function docstrings execute with 0 failures.
2. Source anchors: add(2, 3) -> 5, subtract(10, 4) -> 6, multiply(3, 4) -> 12.
3. Derived neighboring supported inputs: add(3, 4) -> 7, add(2.5, 3.5) -> 6.0, add(0, 0) -> 0.
4. Tracing of the decisive state transition: binary addition x + y.
5. Function purity, idempotence, and absence of side effects.
6. CLI integration: calculator() properly executes and formats add operation.
"""

import builtins
import doctest
import io
import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import simple_calculator
from simple_calculator import add, subtract, multiply, divide, calculator


# ---------------------------------------------------------------------------
# 1. Doctest Execution (Executable Documentation)
# ---------------------------------------------------------------------------


class TestExecutableDocumentationDoctest:
    """Verifies that all docstring worked examples execute successfully via doctest."""

    def test_doctest_execution(self):
        """Execute all doctests in simple_calculator.py and verify zero failures."""
        results = doctest.testmod(simple_calculator, verbose=True)
        assert results.failed == 0, f"Doctest failed: {results}"
        assert results.attempted >= 8, (
            f"Expected at least 8 doctest assertions, got {results.attempted}"
        )


# ---------------------------------------------------------------------------
# 2. Source Anchors & Preconditions
# ---------------------------------------------------------------------------


class TestSourceAnchors:
    """Verifies task-specified source anchors with explicit expected values and citations."""

    def test_anchor_add_2_3(self):
        """Source anchor: add(2, 3) -> 5.

        Source citations:
            - Line 8: module docstring anchor `>>> add(2, 3)`
            - Line 18: `def add(x: float, y: float) -> float:`
            - Line 20: `return x + y` (2 + 3 = 5)
        """
        x, y = 2, 3
        expected = 5
        actual = add(x, y)
        assert actual == expected, (
            f"Anchor add(2, 3) failed: expected {expected}, got {actual}"
        )

    def test_anchor_subtract_10_4(self):
        """Source anchor: subtract(10, 4) -> 6.

        Source citation: Line 10 module docstring anchor `>>> subtract(10, 4)`.
        """
        expected = 6
        actual = subtract(10, 4)
        assert actual == expected

    def test_anchor_multiply_3_4(self):
        """Source anchor: multiply(3, 4) -> 12.

        Source citation: Line 12 module docstring anchor `>>> multiply(3, 4)`.
        """
        expected = 12
        actual = multiply(3, 4)
        assert actual == expected

    def test_module_divide_anchor(self):
        """Module docstring anchor: divide(8, 2) -> 4.0.

        Source citation: Line 14 module docstring `>>> divide(8, 2)`.
        """
        expected = 4.0
        actual = divide(8, 2)
        assert actual == expected


# ---------------------------------------------------------------------------
# 3. Derived Neighboring Supported Inputs
# ---------------------------------------------------------------------------


class TestDerivedNeighborInputs:
    """Verifies independently calculated neighboring supported inputs."""

    def test_derived_neighbor_add_3_4(self):
        """Neighbor derived from anchor multiply(3, 4): add(3, 4) -> 7.

        Preconditions:
            - Source line 18: x=3, y=4
            - Source line 20: 3 + 4 = 7
        """
        expected = 7
        actual = add(3, 4)
        assert actual == expected, f"Neighbor add(3, 4) failed: expected {expected}, got {actual}"

    def test_derived_neighbor_float_add(self):
        """Neighbor with float operands: add(2.5, 3.5) -> 6.0.

        Preconditions:
            - Source line 18: type hint specifies float
            - Source line 20: 2.5 + 3.5 = 6.0
        """
        expected = 6.0
        actual = add(2.5, 3.5)
        assert actual == expected, f"Neighbor add(2.5, 3.5) failed: expected {expected}, got {actual}"

    def test_boundary_zero_addition(self):
        """Boundary case: add(0, 0) -> 0 (additive identity).

        Preconditions:
            - Source line 18: numeric zero inputs
            - Source line 20: 0 + 0 = 0
        """
        expected = 0
        actual = add(0, 0)
        assert actual == expected

    def test_negative_operands_addition(self):
        """Negative operand: add(-5, 5) -> 0 (additive inverse).

        Preconditions:
            - Source line 18: negative and positive float/int
            - Source line 20: -5 + 5 = 0
        """
        expected = 0
        actual = add(-5, 5)
        assert actual == expected

    def test_mixed_sign_addition(self):
        """Mixed signs: add(10, -3) -> 7."""
        expected = 7
        actual = add(10, -3)
        assert actual == expected


# ---------------------------------------------------------------------------
# 4. Tracing the Decisive State Transition
# ---------------------------------------------------------------------------


class TestDecisiveStateTransitionTrace:
    """Traces the decisive state transition from input bindings to final scalar return."""

    def test_trace_integer_addition_transition(self):
        """Trace add(2, 3):
        - State 0 (Input bindings): x = 2, y = 3
        - Decisive Transition: binary evaluation x + y evaluates to 5
        - State 1 (Return): 5
        """
        # State 0: inspect inputs
        x, y = 2, 3
        assert isinstance(x, int)
        assert isinstance(y, int)

        # Decisive state transition
        intermediate_sum = x + y
        assert intermediate_sum == 5

        # Function execution
        result = add(x, y)
        assert result == intermediate_sum == 5

    def test_trace_float_addition_transition(self):
        """Trace add(2.5, 3.5):
        - State 0 (Input bindings): x = 2.5, y = 3.5
        - Decisive Transition: binary evaluation x + y evaluates to 6.0
        - State 1 (Return): 6.0
        """
        x, y = 2.5, 3.5
        assert isinstance(x, float)
        assert isinstance(y, float)

        intermediate_sum = x + y
        assert intermediate_sum == 6.0

        result = add(x, y)
        assert result == intermediate_sum == 6.0


# ---------------------------------------------------------------------------
# 5. Function Purity & Idempotence
# ---------------------------------------------------------------------------


class TestFunctionPurity:
    """Verifies that add() is pure and repeated calls yield identical results."""

    def test_idempotence_and_repeatability(self):
        """Repeated invocations with equivalent inputs produce identical results."""
        first = add(2, 3)
        second = add(2, 3)
        third = add(2, 3)

        assert first == second == third == 5

    def test_argument_immutability(self):
        """Input values remain unchanged across execution."""
        x = 10
        y = 20
        _ = add(x, y)

        assert x == 10
        assert y == 20


# ---------------------------------------------------------------------------
# 6. CLI Integration Verification
# ---------------------------------------------------------------------------


class TestCalculatorCliIntegration:
    """Verifies CLI interactive execution with mocked input and captured stdout."""

    def test_cli_add_execution(self, monkeypatch, capsys):
        """Simulate user selecting option 1 (Add) with inputs 2 and 3."""
        # Simulated user inputs: choice="1", num1="2", num2="3"
        inputs = iter(["1", "2", "3"])
        monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

        calculator()

        captured = capsys.readouterr()
        # Verify the menu and the calculated output
        assert "Select operation." in captured.out
        assert "2.0 + 3.0 = 5.0" in captured.out
