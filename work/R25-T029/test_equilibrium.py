"""Regression and complexity verification tests for equilibrium() in Python-Array-Equilibrium-Index.py.

Contract & Preconditions:
    - Precondition Source Line 46: `total_sum = sum(arr)` (O(N) initial accumulation)
    - Precondition Source Line 47: `leftsum = 0` (prefix sum tracker)
    - Precondition Source Line 48: `for i, num in enumerate(arr):` (O(N) single-pass iteration)
    - Precondition Source Line 51: `total_sum -= num` (O(1) right suffix adjustment)
    - Precondition Source Line 53: `if leftsum == total_sum: return i` (O(1) comparison)
    - Precondition Source Line 55: `leftsum += num` (O(1) left prefix adjustment)
    - Precondition Source Line 59: `return -1` (absence of equilibrium index)

Complexity:
    - Input size variable: N = len(arr)
    - Theoretical worst-case time complexity: O(N)
    - Auxiliary space complexity: O(1)
"""

import importlib.util
import os
import random
import statistics
import sys
import time
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODULE_PATH = os.path.join(REPO_ROOT, "Python-Array-Equilibrium-Index.py")

spec = importlib.util.spec_from_file_location("equilibrium_module", MODULE_PATH)
equilibrium_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(equilibrium_mod)
equilibrium = equilibrium_mod.equilibrium


class TestEquilibriumCorrectnessAndComplexity:
    """Correctness and complexity scaling tests for equilibrium()."""

    def test_smallest_valid_input_single_element(self):
        """Smallest valid input: array of length 1 (arr = [42]).

        Preconditions:
            - Source line 46: total_sum = 42.
            - Source line 51: total_sum -= 42 -> 0.
            - Source line 53: leftsum (0) == total_sum (0) -> returns index 0.

        Input: [42]
        Expected: 0
        """
        literal_input = [42]
        expected = 0
        actual = equilibrium(literal_input)
        assert actual == expected

    def test_ordinary_input_with_equilibrium_index(self):
        """Ordinary input with equilibrium index at position 3.

        Input: [-7, 1, 5, 2, -4, 3, 0]
        Index 3 (value 2):
            Left elements: [-7, 1, 5] -> sum = -1
            Right elements: [-4, 3, 0] -> sum = -1
        Expected: 3
        """
        literal_input = [-7, 1, 5, 2, -4, 3, 0]
        expected = 3
        actual = equilibrium(literal_input)
        assert actual == expected

    def test_ordinary_input_without_equilibrium_index(self):
        """Array with no equilibrium index returns -1."""
        literal_input = [1, 2, 3]
        expected = -1
        actual = equilibrium(literal_input)
        assert actual == expected

    def test_complexity_scaling_experiment_three_sizes(self):
        """Measure the scaling of equilibrium() on 3 increasing sizes with 5 repetitions.

        Input size variable: N = len(arr).
        Sizes: N1 = 5,000, N2 = 20,000, N3 = 80,000.
        All measured cases verify correctness; timings report median and range.
        Note: No test threshold asserts wall-clock speed limits.
        """
        sizes = [5000, 20000, 80000]
        benchmark_summary = {}

        for n in sizes:
            durations = []
            k = n // 2
            # Strictly positive elements guarantee monotonically increasing prefix sums
            # and monotonically decreasing suffix sums, uniquely intersecting at index k.
            fresh_arr = [1] * k + [0] + [1] * k
            expected_index = k

            for rep in range(5):
                # Measure pure algorithm execution (excluding array construction)
                t_start = time.perf_counter()
                actual_index = equilibrium(fresh_arr)
                t_end = time.perf_counter()

                durations.append(t_end - t_start)
                # Correctness checked outside timed interval
                assert actual_index == expected_index, (
                    f"Correctness check failed for N={n}: expected {expected_index}, got {actual_index}"
                )

            median_time = statistics.median(durations)
            time_range = max(durations) - min(durations)
            benchmark_summary[n] = (median_time, time_range)

        assert len(benchmark_summary) == 3
