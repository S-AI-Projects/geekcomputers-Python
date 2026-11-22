"""Focused contract regression tests for four_digit_combinations in four_digit_num_combination.py.

Precondition citations:
    - Line 7: `numbers = []` establishes the accumulation list anchor.
    - Line 8: `for code in range(10000):` establishes upper bound and iteration domain.
    - Line 9: `code = str(code).zfill(4)` establishes 4-digit zero padding format.
    - Line 10: `print(code)` outputs code to stdout.
    - Line 11: `numbers.append(code)` in-place mutation of the accumulation list.
"""

import io
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import four_digit_num_combination as fd


class TestFourDigitCombinationsContract(unittest.TestCase):
    """Tests verifying input/output contract, mutation behavior, and boundary conditions."""

    def test_smallest_valid_input(self):
        """Smallest valid input: limit=1.
        
        Preconditions:
            - Line 7: numbers = []
            - Line 8: range(1) generates single item code=0
            - Line 9: str(0).zfill(4) produces '0000'
        Literal input:
            limit = 1
        Independently calculated expected output:
            ['0000']
        """
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = fd.four_digit_combinations(limit=1)
            self.assertEqual(result, ["0000"])
            self.assertEqual(mock_stdout.getvalue(), "0000\n")

    def test_ordinary_input(self):
        """Ordinary input: limit=5.
        
        Preconditions:
            - Line 7: numbers = []
            - Line 8: range(5) generates sequence [0, 1, 2, 3, 4]
            - Line 9: zfill(4) produces ['0000', '0001', '0002', '0003', '0004']
            - Line 10: stdout outputs lines separated by newline
        Literal input:
            limit = 5
        Independently calculated expected output:
            ['0000', '0001', '0002', '0003', '0004']
        """
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = fd.four_digit_combinations(limit=5)
            expected = ["0000", "0001", "0002", "0003", "0004"]
            self.assertEqual(result, expected)
            self.assertEqual(mock_stdout.getvalue(), "0000\n0001\n0002\n0003\n0004\n")

    def test_observable_mutation_separate_from_return(self):
        """Separate test for observable mutation on passed list fixture.
        
        Preconditions:
            - Line 7: numbers fixture
            - Line 11: numbers.append(code) mutates passed list in place
        Literal input:
            limit = 3, numbers = []
        Independently calculated expected output:
            The fixture list itself is mutated to ['0000', '0001', '0002']
        """
        numbers_fixture = []
        with patch("sys.stdout", new_callable=io.StringIO):
            return_val = fd.four_digit_combinations(limit=3, numbers=numbers_fixture)
            # Observable mutation check on the fixture object
            self.assertIs(return_val, numbers_fixture)
            self.assertEqual(numbers_fixture, ["0000", "0001", "0002"])

    def test_boundary_zero_limit(self):
        """Smallest supported boundary: limit=0 (empty execution).
        
        Preconditions:
            - Line 8: range(0) terminates immediately without iterating
        Literal input:
            limit = 0
        Independently calculated expected output:
            [] (empty list, empty stdout)
        """
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = fd.four_digit_combinations(limit=0)
            self.assertEqual(result, [])
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_boundary_padding_transition(self):
        """Domain boundary: zero-padding transition from 1-digit to 2-digit numbers.
        
        Preconditions:
            - Line 9: str(code).zfill(4) preserves 4 characters across decade boundary (9 -> '0009', 10 -> '0010')
        Literal input:
            limit = 11
        Independently calculated expected output:
            Index 9: '0009', Index 10: '0010'
        """
        with patch("sys.stdout", new_callable=io.StringIO):
            result = fd.four_digit_combinations(limit=11)
            self.assertEqual(result[9], "0009")
            self.assertEqual(result[10], "0010")
            self.assertEqual(len(result), 11)


if __name__ == "__main__":
    unittest.main()
