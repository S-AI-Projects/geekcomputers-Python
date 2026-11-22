"""Cross-check tests comparing Randomnumber against an independent reference implementation.

Precondition citations:
    - Source Line 4: `from random import randint`
    - Source Line 6: `randint(0, 9)` defines standard interval [0, 9]
"""

import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import Randomnumber as rn


def reference_rng(start: int, end: int, prng: random.Random) -> int:
    """Independent reference implementation using randrange on an isolated Random instance."""
    return prng.randrange(start, end + 1)


class TestRandomNumberCrossCheck:
    """Differential testing against independent reference implementation under controlled PRNG state."""

    def test_smallest_valid_input_zero_range(self):
        """Smallest valid input: start=0, end=0 (domain size 1).

        Preconditions:
            - Source line 4: randint(0, 0)
            - Source line 6: Bound interval [0, 0]
        Literal input:
            start=0, end=0
        Independently calculated expected output:
            0 (deterministic, regardless of seed)
        """
        result = rn.random_number(0, 0)
        assert result == 0
        assert rn.Randomnumber(0, 0) == 0

        # Cross check against independent reference
        ref_prng = random.Random(12345)
        ref_val = reference_rng(0, 0, ref_prng)
        assert result == ref_val == 0

    def test_ordinary_input_fixed_seed(self):
        """Ordinary input: start=0, end=9 under controlled seed.

        Preconditions:
            - Source line 4: randint(0, 9)
            - Source line 6: Default parameters 0, 9
        Literal input:
            start=0, end=9, seed=42
        Independently calculated expected output:
            With standard Python random.seed(42), randint(0, 9) yields 1.
        """
        random.seed(42)
        val = rn.random_number(0, 9)
        assert isinstance(val, int)
        assert 0 <= val <= 9

        # Independent reference check with fresh seed 42
        ref_prng = random.Random(42)
        ref_val = reference_rng(0, 9, ref_prng)
        assert val == ref_val

    def test_cross_check_equivalence_across_seeds(self):
        """Full domain cross-check: Compares Randomnumber and independent reference across 50 seeds."""
        for seed in range(50):
            # Controlled state for system random
            random.seed(seed)
            actual = rn.random_number(0, 9)

            # Controlled state for reference
            ref_prng = random.Random(seed)
            expected = reference_rng(0, 9, ref_prng)

            assert actual == expected, f"Discrepancy at seed {seed}: {actual} != {expected}"
            assert 0 <= actual <= 9

    def test_output_type_and_argument_isolation(self):
        """Checks output shape, integer type, and guarantees arguments remain unmutated."""
        start = 2
        end = 7
        val = rn.random_number(start, end)
        assert type(val) is int
        assert 2 <= val <= 7
        assert start == 2
        assert end == 7
