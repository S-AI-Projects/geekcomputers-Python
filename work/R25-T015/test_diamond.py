"""Focused repeatability and deterministic execution tests for draw_diamond in diamond.py.

Precondition citations:
    - Line 1: `def draw_diamond(n):` input interface.
    - Line 2: `if n % 2 != 0:` establishes parity precondition (odd integer).
    - Line 4-5: `k <= n` upper half expansion with symmetric padding.
    - Line 9-10: `(n - 2*j) >= 1` lower half contraction with symmetric padding.
    - Line 14: Rejection message for even integers.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import diamond


class TestDiamondDeterministicExecution(unittest.TestCase):
    """Tests verifying repeatable output, dependency seam injection, and input isolation."""

    def test_smallest_valid_input_one(self):
        """Smallest valid input: n=1.
        
        Preconditions:
            - Line 2: 1 % 2 != 0 (odd)
            - Line 4-5: k=1, (1-1)/2=0 spaces -> '*'
            - Line 9: (1 - 2*1) = -1 < 1 -> lower loop terminates
        Literal input:
            n = 1
        Independently calculated expected output:
            ["*"]
        """
        lines = []
        diamond.draw_diamond(1, output_fn=lines.append)
        self.assertEqual(lines, ["*"])

    def test_ordinary_input_three(self):
        """Ordinary input: n=3.
        
        Preconditions:
            - Line 2: 3 % 2 != 0 (odd)
            - Line 4-5: k=1 -> ' * ', k=3 -> '***'
            - Line 9-10: j=1 -> ' * '
        Literal input:
            n = 3
        Independently calculated expected output:
            [" * ", "***", " * "]
        """
        lines = []
        diamond.draw_diamond(3, output_fn=lines.append)
        expected = [" * ", "***", " * "]
        self.assertEqual(lines, expected)

    def test_ordinary_input_five(self):
        """Ordinary input: n=5.
        
        Literal input:
            n = 5
        Independently calculated expected output:
            ["  *  ", " *** ", "*****", " *** ", "  *  "]
        """
        lines = []
        diamond.draw_diamond(5, output_fn=lines.append)
        expected = ["  *  ", " *** ", "*****", " *** ", "  *  "]
        self.assertEqual(lines, expected)

    def test_even_number_rejection(self):
        """Even input rejection: n=4.
        
        Preconditions:
            - Line 14: else branch prints rejection message
        Literal input:
            n = 4
        Independently calculated expected output:
            ["Not an odd number. Can't draw a diamond :("]
        """
        lines = []
        diamond.draw_diamond(4, output_fn=lines.append)
        self.assertEqual(lines, ["Not an odd number. Can't draw a diamond :("])

    def test_repeatability_and_input_isolation(self):
        """Assert that running a fixture twice with an intervening distinct call produces identical output."""
        run1_lines = []
        diamond.draw_diamond(3, output_fn=run1_lines.append)

        # Intervening run with different input
        intervening_lines = []
        diamond.draw_diamond(7, output_fn=intervening_lines.append)
        self.assertEqual(len(intervening_lines), 7)

        # Repeat run of first fixture
        run2_lines = []
        diamond.draw_diamond(3, output_fn=run2_lines.append)

        # Verification: Earlier runs cannot alter subsequent results
        self.assertEqual(run1_lines, run2_lines)
        self.assertEqual(run2_lines, [" * ", "***", " * "])


if __name__ == "__main__":
    unittest.main()
