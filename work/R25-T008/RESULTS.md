# Verification Evidence — R25-T008

## Target
- **Script:** calc_area.py
- **Function:** `main`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest /Users/krishna/SnAIproject/work/R25-T008/test_calc_area.py -v --tb=short`

## Precondition Citations
- Line 5: `shape = int(...)` input parsing
- Line 11: `shape == 1` square area formula
- Line 14: `shape == 2` rectangle area formula
- Line 32: `else: print("You have selected wrong choice.")` failure fallback branch
- Line 35: `restart = input(...)` loop control

## Failure Branch & Validity Matrix
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Documented failure branch | L5, L32 | `shape=9, restart='n'` | `"You have selected wrong choice."` | `"You have selected wrong choice."` | PASS |
| Smallest valid input | L11 | `shape=1, side=0.0` | `"Area of square = 0.0"` | `"Area of square = 0.0"` | PASS |
| Ordinary valid input | L11 | `shape=1, side=5.0` | `"Area of square = 25.0"` | `"Area of square = 25.0"` | PASS |
| Valid call after failure | L14, L32 | `shape=99` then `shape=2` | Failure handled, rectangle area 20.0 computed | Both calls succeeded | PASS |

## Test Runner Output
```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.14/bin/python3
cachedir: .pytest_cache
rootdir: /Users/krishna/SnAIproject
collecting ... collected 4 items

work/R25-T008/test_calc_area.py::TestCalcAreaFailureAndContracts::test_documented_failure_branch_wrong_choice PASSED [ 25%]
work/R25-T008/test_calc_area.py::TestCalcAreaFailureAndContracts::test_smallest_valid_input_zero_side_square PASSED [ 50%]
work/R25-T008/test_calc_area.py::TestCalcAreaFailureAndContracts::test_ordinary_valid_input PASSED [ 75%]
work/R25-T008/test_calc_area.py::TestCalcAreaFailureAndContracts::test_ordinary_call_succeeds_after_failure_case PASSED [100%]

============================== 4 passed in 0.02s ===============================
```

**Exit Code:** 0
