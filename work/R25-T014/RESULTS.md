# Verification Evidence — R25-T014

## Target
- **Script:** Python Distance.py
- **Function:** `python_distance`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m unittest /Users/nevilmaru009/.gemini/antigravity/scratch/geekcomputers-Python/work/R25-T014/test_python_distance.py -v`

## Precondition Citations
- Line 3: `terms = 10` establishes default iteration terms fixture.
- Line 9: `result = list(map(lambda x: 2**x, range(terms)))` defines the functional calculation.

## Mathematical Invariants
- **Shape Invariant:** For any non-negative integer `terms`, output is a `list` with `len(result) == terms`.
- **Base Invariant:** `result[0] == 1` when `terms >= 1`.
- **Recurrence Invariant:** `result[i+1] == 2 * result[i]` for all consecutive indices.
- **Bit-level Equivalence:** `result[i] == (1 << i)` for all `0 <= i < terms`.
- **Monotonicity:** `result[i] < result[i+1]` strictly increasing for all `i`.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (zero) | L9 | `terms=0` | `[]` | `[]` | PASS |
| Smallest positive input (one) | L9 | `terms=1` | `[1]` | `[1]` | PASS |
| Ordinary input (ten) | L3, L9 | `terms=10` | `[1, 2, ..., 512]` | Exact 10-element list | PASS |
| 100 Bounded Property Cases | L3, L9 | 100 random `terms in [0..60]` (seed=42) | All 4 invariants hold | 100/100 passed | PASS |
| Mutation resistance check | L9 | Mutant `2**x + 1` | Detects recurrence violation | Violation detected | PASS |

## Test Runner Output
```
test_100_bounded_cases_invariants (work.R25-T014.test_python_distance.TestPythonDistanceProperties.test_100_bounded_cases_invariants)
Evaluate invariant properties over 100 bounded cases with a fixed deterministic seed. ... ok
test_invariant_violation_detects_mutant (work.R25-T014.test_python_distance.TestPythonDistanceProperties.test_invariant_violation_detects_mutant)
Demonstrate that an intentional mutation (e.g. 2**x + 1) violates the invariant. ... ok
test_ordinary_input_ten (work.R25-T014.test_python_distance.TestPythonDistanceProperties.test_ordinary_input_ten)
Ordinary input: terms=10 (matching source line 3 fixture). ... ok
test_smallest_valid_input_one (work.R25-T014.test_python_distance.TestPythonDistanceProperties.test_smallest_valid_input_one)
Smallest positive input: terms=1. ... ok
test_smallest_valid_input_zero (work.R25-T014.test_python_distance.TestPythonDistanceProperties.test_smallest_valid_input_zero)
Smallest valid input: terms=0. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

**Exit Code:** 0
