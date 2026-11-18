# Verification Evidence — R25-T029 (Python-Array-Equilibrium-Index.py)

## Environment & Tool Versions
- **Python Version:** 3.13.14
- **Platform:** macOS-27.3-arm64-arm-64bit-Mach-O
- **Runner:** /Users/namanlunia/SandAI/.venv/bin/python3
- **Target File:** Python-Array-Equilibrium-Index.py (function `equilibrium`)
- **Test Suite:** work/R25-T029/test_equilibrium.py

## Executed Command
```bash
/Users/namanlunia/SandAI/.venv/bin/python3 -m pytest -v /Users/namanlunia/SandAI/geekcomputers-Python/work/R25-T029/test_equilibrium.py
```

## Complexity Statement
- **Input Size Variable:** `N = len(arr)` (number of elements).
- **Theoretical Worst-Case:** $O(N)$ time, $O(1)$ auxiliary space.
- **Empirical Observations:** Timing scales approximately linearly with $N$ across $N \in [5000, 20000, 80000]$.

## Empirical Scaling Benchmarks (5 Repetitions per Size)
| Input Size N | Median Duration (s) | Min Duration (s) | Max Duration (s) | Range (s) | Correctness Checked |
|---|---|---|---|---|---|
| 5,000 | 0.000072 | 0.000071 | 0.000076 | 0.000005 | PASS |
| 20,000 | 0.000284 | 0.000277 | 0.000293 | 0.000016 | PASS |
| 80,000 | 0.001140 | 0.001118 | 0.001152 | 0.000034 | PASS |

## Precondition Source Lines Cited
- `Python-Array-Equilibrium-Index.py#L46`: `total_sum = sum(arr)` (O(N) sum calculation)
- `Python-Array-Equilibrium-Index.py#L47`: `leftsum = 0` (prefix sum accumulator)
- `Python-Array-Equilibrium-Index.py#L48`: `for i, num in enumerate(arr):` (single pass loop)
- `Python-Array-Equilibrium-Index.py#L51`: `total_sum -= num` (O(1) right sum update)
- `Python-Array-Equilibrium-Index.py#L53`: `if leftsum == total_sum: return i` (O(1) equilibrium check)
- `Python-Array-Equilibrium-Index.py#L55`: `leftsum += num` (O(1) left sum update)
- `Python-Array-Equilibrium-Index.py#L59`: `return -1` (unsuccessful termination)

## Pytest Console Output
```
============================= test session starts ==============================
platform darwin -- Python 3.13.14, pytest-9.2.0, pluggy-1.7.0 -- /Users/namanlunia/SandAI/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/namanlunia/SandAI/geekcomputers-Python
collecting ... collected 4 items

work/R25-T029/test_equilibrium.py::TestEquilibriumCorrectnessAndComplexity::test_smallest_valid_input_single_element PASSED [ 25%]
work/R25-T029/test_equilibrium.py::TestEquilibriumCorrectnessAndComplexity::test_ordinary_input_with_equilibrium_index PASSED [ 50%]
work/R25-T029/test_equilibrium.py::TestEquilibriumCorrectnessAndComplexity::test_ordinary_input_without_equilibrium_index PASSED [ 75%]
work/R25-T029/test_equilibrium.py::TestEquilibriumCorrectnessAndComplexity::test_complexity_scaling_experiment_three_sizes PASSED [100%]

============================== 4 passed in 0.03s ===============================

```

**Exit Code:** 0
