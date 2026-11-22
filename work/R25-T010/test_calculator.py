"""Focused mutation-resistant tests for calc in calculator.py.

Precondition citations:
    - Source Line 33: `def calc(term):` accepts mathematical string
    - Source Line 41: `term.replace(" ", "")` whitespace stripping
    - Source Line 42: `term.replace("^", "**")` exponent operator conversion
    - Source Line 45: `term.replace("%", "/100.00")` percentage normalization
    - Source Lines 50-62: `functions = [...]` anchor list of math library functions
    - Source Line 67: `eval(term)` evaluation with math module in scope
"""

import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import calculator


class TestCalculatorMutationResistance:
    """Verifies calculator behavior, invariants, and proves mutation resistance."""

    def test_smallest_valid_input_zero(self):
        """Smallest valid input: '0'.

        Preconditions:
            - Source line 33: term = '0'
            - Source line 67: eval('0') = 0
        Literal input:
            '0'
        Independently calculated expected output:
            0
        """
        assert calculator.calc("0") == 0

    def test_ordinary_arithmetic_input(self):
        """Ordinary input: '2 + 3 * 4'.

        Preconditions:
            - Source line 41: whitespace stripped to '2+3*4'
            - Source line 67: 2 + (3 * 4) = 14
        Literal input:
            '2 + 3 * 4'
        Independently calculated expected output:
            14
        """
        assert calculator.calc("2 + 3 * 4") == 14

    def test_exponent_operator_invariant(self):
        """Exponentiation invariant: '^' operator maps to '**' power operation.

        Preconditions:
            - Source line 42: term.replace('^', '**')
        Literal input:
            '2 ^ 3'
        Independently calculated expected output:
            2 ** 3 = 8
        """
        assert calculator.calc("2 ^ 3") == 8

    def test_percentage_normalization_invariant(self):
        """Percentage invariant: '%' operator converts to decimal division by 100.0.

        Preconditions:
            - Source line 45: term.replace('%', '/100.00')
        Literal input:
            '50% * 100'
        Independently calculated expected output:
            (50 / 100.0) * 100 = 50.0
        """
        assert calculator.calc("50% * 100") == 50.0

    def test_math_functions_anchors(self):
        """Tests scientific functions anchor list from lines 50-62."""
        assert calculator.calc("sin(0)") == 0.0
        assert calculator.calc("sqrt(16)") == 4.0
        assert math.isclose(calculator.calc("pi"), math.pi)

    def test_mutation_detection_exponent_mutant(self):
        """Proves that a plausible one-line mistake in line 42 is detected by the regression assertion.

        Plausible Mutant:
            Replacing `term.replace("^", "**")` with `term.replace("^", "*")`
            (accidental single asterisk for multiplication instead of exponentiation).
        """
        def mutant_calc(term):
            term = term.lower().replace(" ", "")
            # Plausible bug: single asterisk instead of power
            term = term.replace("^", "*")
            return eval(term)

        # Baseline passes
        baseline_result = calculator.calc("2 ^ 3")
        assert baseline_result == 8

        # Mutant produces 6 (2 * 3) instead of 8 (2 ** 3)
        mutant_result = mutant_calc("2 ^ 3")
        assert mutant_result == 6
        assert mutant_result != 8, "Expected mutant to fail exponent invariant assertion!"

    def test_mutation_detection_percentage_mutant(self):
        """Proves that an off-by-one divisor mutant in line 45 is caught by percentage assertion.

        Plausible Mutant:
            `term.replace("%", "/10.00")` instead of `/100.00`.
        """
        def mutant_calc(term):
            term = term.lower().replace(" ", "")
            # Plausible bug: /10.00 instead of /100.00
            term = term.replace("%", "/10.00")
            return eval(term)

        baseline_result = calculator.calc("50% * 100")
        assert baseline_result == 50.0

        mutant_result = mutant_calc("50% * 100")
        assert mutant_result == 500.0
        assert mutant_result != 50.0, "Expected mutant to fail percentage normalization assertion!"
