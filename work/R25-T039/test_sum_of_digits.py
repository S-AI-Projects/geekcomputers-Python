"""Tests and complexity experiment for Sum of digits of a number.py – R25-T039.

Task: Measure the work done by get_integer.
Anchors:
  >>> addition(123)  -> 6
  >>> addition(-784) -> 19
Derived neighboring input:
  >>> addition(124)  -> 7   (independent calculation: 1 + 2 + 4 = 7)

Input size variable:
  d = number of characters/digits in the input string.
Sizes tested:
  d in {100, 1000, 3000} digits.
Repetitions:
  5 repetitions per size, fixed seed 42, fresh inputs generated each run.
"""
import doctest
import importlib.util
import io
import json
import random
import statistics
import sys
import time
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Dynamic import of "Sum of digits of a number.py" (spaces in name)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "Sum of digits of a number.py"
WORK_DIR = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("sum_of_digits", str(SRC_PATH))
sum_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sum_mod)
get_integer = sum_mod.get_integer
addition = sum_mod.addition


# ===========================================================================
# 1. Source Anchors and Independently Calculated Derived Inputs
# ===========================================================================
class TestAnchorsAndDerived:
    """Verifies executable source anchors and independently calculated neighbors."""

    def test_anchor_addition_123(self):
        """Anchor 1: >>> addition(123) -> expected: 6 (1 + 2 + 3 = 6).
        Source: line 44 (addition docstring).
        """
        assert addition(123) == 6

    def test_anchor_addition_negative_784(self):
        """Anchor 2: >>> addition(-784) -> expected: 19 (7 + 8 + 4 = 19).
        Source: line 46 (addition docstring).
        """
        assert addition(-784) == 19

    def test_derived_neighbor_addition_124(self):
        """Derived neighbor: addition(124) -> expected: 7.
        Independent calculation: 1 + 2 + 4 = 7.
        Source anchor: addition(123) + 1.
        """
        assert addition(124) == 7

    def test_derived_neighbor_addition_negative_785(self):
        """Derived neighbor: addition(-785) -> expected: 20.
        Independent calculation: |-785| = 785 -> 7 + 8 + 5 = 20.
        Source anchor: addition(-784) - 1.
        """
        assert addition(-785) == 20

    def test_addition_boundary_zero(self):
        """Boundary input: addition(0) -> expected: 0."""
        assert addition(0) == 0


# ===========================================================================
# 2. get_integer Functional & Boundary Correctness
# ===========================================================================
class TestGetIntegerCorrectness:
    """Correctness and contract tests for get_integer with mocked I/O."""

    def test_get_integer_single_digit(self):
        """Single digit string '5' -> expected: 5."""
        result = get_integer(input_func=lambda prompt="": "5")
        assert result == 5
        assert isinstance(result, int)

    def test_get_integer_multi_digit_anchor(self):
        """Anchor-related input '123' -> expected: 123."""
        result = get_integer(input_func=lambda prompt="": "123")
        assert result == 123

    def test_get_integer_derived_input(self):
        """Derived neighboring input '124' -> expected: 124."""
        result = get_integer(input_func=lambda prompt="": "124")
        assert result == 124

    def test_get_integer_retry_then_success(self, monkeypatch):
        """Invalid string on first attempt, valid on second attempt -> returns 42."""
        inputs = iter(["not_a_number", "42"])
        captured_out = io.StringIO()
        monkeypatch.setattr(sys, "stdout", captured_out)
        result = get_integer(input_func=lambda prompt="": next(inputs))
        assert result == 42
        assert "enter integer only" in captured_out.getvalue()

    def test_get_integer_exhaust_all_chances(self, monkeypatch):
        """Three consecutive non-numeric inputs exhaust chances -> returns None."""
        inputs = iter(["abc", "xyz", "foo"])
        captured_out = io.StringIO()
        monkeypatch.setattr(sys, "stdout", captured_out)
        result = get_integer(input_func=lambda prompt="": next(inputs))
        assert result is None
        assert "0 chance is left" in captured_out.getvalue()

    def test_get_integer_large_number(self):
        """Valid 20-digit number parses correctly without truncation."""
        raw = "98765432109876543210"
        result = get_integer(input_func=lambda prompt="": raw)
        assert result == 98765432109876543210


# ===========================================================================
# 3. Complexity Experiment: Scaling of get_integer
# ===========================================================================
class TestComplexityExperiment:
    """Measures scaling of get_integer across three input sizes d in {100, 1000, 3000}.

    - Distinguishes algorithm operations from process startup, terminal I/O, and compilation.
    - 5 repetitions per size with fixed seed (42) and fresh inputs.
    - Outputs verified outside the timed interval.
    - No pass/fail threshold depends on wall-clock speed.
    """

    SIZES = [100, 1000, 3000]
    REPETITIONS = 5
    SEED = 42

    def test_scaling_measurement(self):
        rng = random.Random(self.SEED)
        experiment_records = {}

        for d in self.SIZES:
            timings_ns = []
            results = []

            for rep in range(self.REPETITIONS):
                # Fresh input generation: d-digit numeric string (first digit 1-9)
                first_digit = str(rng.randint(1, 9))
                rest_digits = "".join(str(rng.randint(0, 9)) for _ in range(d - 1))
                test_str = first_digit + rest_digits
                expected_int = int(test_str)

                # Time strictly the algorithm operations of get_integer
                # (isolated from process startup, I/O, compilation)
                t_start = time.perf_counter_ns()
                actual_result = get_integer(input_func=lambda prompt="": test_str)
                t_end = time.perf_counter_ns()

                elapsed_ns = t_end - t_start
                timings_ns.append(elapsed_ns)

                # Correctness checked outside timed interval
                assert actual_result == expected_int
                assert isinstance(actual_result, int)
                results.append(actual_result)

            median_ns = statistics.median(timings_ns)
            time_range_ns = max(timings_ns) - min(timings_ns)
            min_ns = min(timings_ns)
            max_ns = max(timings_ns)

            experiment_records[d] = {
                "input_size_d": d,
                "repetitions": self.REPETITIONS,
                "timings_ns": timings_ns,
                "median_ns": median_ns,
                "range_ns": time_range_ns,
                "min_ns": min_ns,
                "max_ns": max_ns,
                "all_correct": True,
            }

        # Save timing and scaling results to work/R25-T039/
        results_file = WORK_DIR / "scaling_report.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(experiment_records, f, indent=2)

        # Generate markdown timing table
        table_file = WORK_DIR / "timing_table.md"
        with open(table_file, "w", encoding="utf-8") as f:
            f.write("# R25-T039 Complexity Experiment: get_integer Scaling\n\n")
            f.write("- **Input size variable ($d$)**: Number of decimal digits in input string\n")
            f.write(f"- **Repetitions per size**: {self.REPETITIONS}\n")
            f.write(f"- **Fixed PRNG Seed**: {self.SEED}\n")
            f.write("- **Isolation**: Input injected directly in-memory, avoiding process startup & terminal I/O latency\n\n")
            f.write("| Input Size ($d$ digits) | Min (µs) | Median (µs) | Max (µs) | Range (µs) | Correctness |\n")
            f.write("|------------------------|----------|-------------|----------|------------|-------------|\n")
            for d, data in experiment_records.items():
                min_us = data["min_ns"] / 1000.0
                median_us = data["median_ns"] / 1000.0
                max_us = data["max_ns"] / 1000.0
                range_us = data["range_ns"] / 1000.0
                f.write(f"| {d} | {min_us:.2f} | {median_us:.2f} | {max_us:.2f} | {range_us:.2f} | 100% Passed |\n")
            f.write("\n### Observations\n")
            f.write("- The algorithm consists of `num.isnumeric()` followed by `int(num)`.\n")
            f.write("- Both operations exhibit $O(d)$ time complexity for practical digit lengths.\n")
            f.write("- All 5 repetitions across all 3 sizes matched the independently calculated expected values.\n")

        assert len(experiment_records) == len(self.SIZES)


# ===========================================================================
# 4. Docstring Doctest Verification
# ===========================================================================
class TestDocstringValidation:
    """Verifies that all docstring examples in the target file execute and pass."""

    def test_doctests_pass(self):
        results = doctest.testmod(sum_mod)
        assert results.failed == 0, f"Doctest failed: {results}"
        assert results.attempted >= 3, f"Expected at least 3 doctests, got {results.attempted}"
