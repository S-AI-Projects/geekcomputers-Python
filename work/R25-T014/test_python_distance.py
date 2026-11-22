"""Focused property and invariant tests for Python Distance in Python Distance.py.

Precondition citations:
    - Line 3: `terms = 10` establishes default iteration count anchor.
    - Line 9: `result = list(map(lambda x: 2**x, range(terms)))` functional mapping.
    - Mathematical Invariant: For all non-negative integers n, output length is n,
      result[i] == 2**i == 1 << i, and result[i+1] == 2 * result[i].
"""

import importlib.util
import random
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = REPO_ROOT / "Python Distance.py"

# Import module with space in filename dynamically
spec = importlib.util.spec_from_file_location("python_distance_mod", str(TARGET_FILE))
pydist = importlib.util.module_from_spec(spec)
sys.modules["python_distance_mod"] = pydist
spec.loader.exec_module(pydist)


class TestPythonDistanceProperties(unittest.TestCase):
    """Property-based invariant testing with deterministic pseudo-random seeds."""

    def test_smallest_valid_input_zero(self):
        """Smallest valid input: terms=0.
        
        Preconditions:
            - Line 9: range(0) produces empty iteration
        Literal input:
            terms = 0
        Independently calculated expected output:
            [] (empty list)
        """
        res = pydist.python_distance(0)
        self.assertEqual(res, [])
        self.assertEqual(len(res), 0)

    def test_smallest_valid_input_one(self):
        """Smallest positive input: terms=1.
        
        Preconditions:
            - Line 9: 2**0 == 1
        Literal input:
            terms = 1
        Independently calculated expected output:
            [1]
        """
        res = pydist.python_distance(1)
        self.assertEqual(res, [1])

    def test_ordinary_input_ten(self):
        """Ordinary input: terms=10 (matching source line 3 fixture).
        
        Preconditions:
            - Line 3: terms = 10
            - Line 9: 2**x for x in [0..9]
        Literal input:
            terms = 10
        Independently calculated expected output:
            [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        """
        expected = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        res = pydist.python_distance(10)
        self.assertEqual(res, expected)
        self.assertEqual(pydist.result, expected)

    def test_100_bounded_cases_invariants(self):
        """Evaluate invariant properties over 100 bounded cases with a fixed deterministic seed."""
        rng = random.Random(42)
        test_cases = [rng.randint(0, 60) for _ in range(100)]

        for idx, n in enumerate(test_cases):
            with self.subTest(iteration=idx, terms=n):
                res = pydist.python_distance(n)

                # Invariant 1: Length and type shape
                self.assertIsInstance(res, list)
                self.assertEqual(len(res), n)

                # Invariant 2: Base element
                if n > 0:
                    self.assertEqual(res[0], 1)

                # Invariant 3: Recurrence and bit-shift equality
                for i in range(n):
                    self.assertEqual(res[i], 1 << i)
                    if i + 1 < n:
                        self.assertEqual(res[i + 1], 2 * res[i])
                        self.assertLess(res[i], res[i + 1])

    def test_invariant_violation_detects_mutant(self):
        """Demonstrate that an intentional mutation (e.g. 2**x + 1) violates the invariant."""
        mutant_fn = lambda terms: list(map(lambda x: 2**x + 1, range(terms)))
        bad_result = mutant_fn(5)
        # Recurrence check fails: 2*bad_result[0] == 4 != bad_result[1] (which is 3)
        self.assertNotEqual(bad_result[1], 2 * bad_result[0])


if __name__ == "__main__":
    unittest.main()
