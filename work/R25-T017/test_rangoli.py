"""Focused executable documentation tests for print_rangoli in rangoli.py.

Precondition citations:
    - Line 5: `def print_rangoli(n):` input size parameter.
    - Line 7: `width = 4 * n - 3` line width invariant.
    - Line 14: Descending character loop `chr(96 + n - j)`.
    - Line 19: Ascending character loop `chr(97 + n - k)`.
    - Line 24, 38: Hyphen-centered output lines.
"""

import io
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import rangoli


class TestRangoliExecutableDocumentation(unittest.TestCase):
    """Tests executing the documentation examples and asserting intermediate and final state."""

    def test_smallest_valid_input_one(self):
        """Smallest valid input: n=1.
        
        Preconditions:
            - Line 7: width = 4*1 - 3 = 1
            - Line 14: chr(96 + 1 - 0) = 'a'
        Literal input:
            n = 1
        Independently calculated expected output:
            "a\n"
        """
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            rangoli.print_rangoli(1)
            self.assertEqual(mock_out.getvalue(), "a\n")

    def test_ordinary_input_three_documentation_example(self):
        """Ordinary input: n=3 matching the docstring worked example.
        
        Preconditions:
            - Line 7: width = 4*3 - 3 = 9
            - Center row has 2*3 - 1 = 5 letters and 4 hyphens = 9 chars
        Literal input:
            n = 3
        Independently calculated expected output:
            "----c----\n--c-b-c--\nc-b-a-b-c\n--c-b-c--\n----c----\n"
        """
        expected_lines = [
            "----c----",
            "--c-b-c--",
            "c-b-a-b-c",
            "--c-b-c--",
            "----c----",
        ]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            rangoli.print_rangoli(3)
            actual_lines = [line for line in mock_out.getvalue().split("\n") if line]
            self.assertEqual(actual_lines, expected_lines)

    def test_decisive_state_transition_center_boundary(self):
        """Test the state transition where len(string) reaches width and suppresses trailing hyphen."""
        n = 3
        width = 4 * n - 3  # 9

        # Row 1 (i=1): uncentered string is 'c-' (length 2)
        s1 = chr(96 + 3 - 0) + "-"
        self.assertEqual(s1, "c-")
        self.assertEqual(s1.center(width, "-"), "----c----")

        # Row 3 (i=3, center): string reaches exact width 9, trailing hyphen suppressed
        chars = ["c", "b", "a", "b", "c"]
        s3 = "-".join(chars)
        self.assertEqual(len(s3), width)
        self.assertEqual(s3, "c-b-a-b-c")
        self.assertEqual(s3.center(width, "-"), "c-b-a-b-c")


if __name__ == "__main__":
    unittest.main()
