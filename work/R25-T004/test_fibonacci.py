"""Invariant and property tests for Fibonacci sequence generation in how to display the fibonacci sequence up to n-.py.

Precondition citations:
    - Source Line 6: `n1, n2 = 0, 1` defines initial base values F(0)=0 and F(1)=1.
    - Source Line 10: `nterms <= 0` bounds domain to positive counts.
    - Source Line 17: `nth = n1 + n2` recurrence relation establishing F(n+2) = F(n+1) + F(n).
"""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TARGET_PATH = REPO_ROOT / "how to display the fibonacci sequence up to n-.py"
spec = importlib.util.spec_from_file_location("fib_mod", str(TARGET_PATH))
fib_mod = importlib.util.module_from_spec(spec)
sys.modules["fib_mod"] = fib_mod
spec.loader.exec_module(fib_mod)


class TestFibonacciInvariant:
    """Tests establishing fixture values, property invariants, and mutation detection."""

    def test_fixture_values_at_specified_indices(self):
        """Validates exact values at indices 0, 1, 2, 5, and 10 against fixture requirements.

        Fixture:
            Conventional zero-based indices:
            F(0) = 0
            F(1) = 1
            F(2) = 1
            F(5) = 5
            F(10) = 55
        """
        # Generate 11 terms so index 10 is populated
        seq = fib_mod.fibonacci_sequence(11)
        assert len(seq) == 11

        assert seq[0] == 0, f"Expected F(0)=0, got {seq[0]}"
        assert seq[1] == 1, f"Expected F(1)=1, got {seq[1]}"
        assert seq[2] == 1, f"Expected F(2)=1, got {seq[2]}"
        assert seq[5] == 5, f"Expected F(5)=5, got {seq[5]}"
        assert seq[10] == 55, f"Expected F(10)=55, got {seq[10]}"

        # Alias check
        alias_seq = fib_mod.how_to_display_the_fibonacci_sequence_up_to_n(11)
        assert alias_seq == seq

    def test_recurrence_invariant_across_range(self):
        """Validates property invariant: For all supported indices n, F(n+2) == F(n+1) + F(n)."""
        seq = fib_mod.fibonacci_sequence(25)
        for n in range(len(seq) - 2):
            lhs = seq[n + 2]
            rhs = seq[n + 1] + seq[n]
            assert lhs == rhs, f"Invariant violated at index {n}: {lhs} != {rhs}"

    def test_smallest_valid_input_boundaries(self):
        """Validates smallest supported input boundaries: 0, 1, and 2 terms."""
        assert fib_mod.fibonacci_sequence(0) == []
        assert fib_mod.fibonacci_sequence(1) == [0]
        assert fib_mod.fibonacci_sequence(2) == [0, 1]

    def test_deliberate_mutant_fails_invariant(self):
        """Demonstrates that a deliberate mutation breaking F(n+2) = F(n+1) + F(n) is detected."""
        def mutant_fibonacci(nterms):
            if nterms <= 0:
                return []
            if nterms == 1:
                return [0]
            n1, n2 = 0, 1
            terms = []
            while len(terms) < nterms:
                terms.append(n1)
                # Deliberate plausible off-by-one addition mutant
                nth = n1 + n2 + 1
                n1 = n2
                n2 = nth
            return terms

        mutant_seq = mutant_fibonacci(10)
        # Verify the invariant check catches this discrepancy
        invariant_broken = False
        for n in range(len(mutant_seq) - 2):
            if mutant_seq[n + 2] != mutant_seq[n + 1] + mutant_seq[n]:
                invariant_broken = True
                break
        assert invariant_broken, "Expected invariant failure on mutant was not detected!"
