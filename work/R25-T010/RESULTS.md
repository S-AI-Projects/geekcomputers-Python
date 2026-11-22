# Verification Evidence — R25-T010

## Target
- **Script:** calculator.py
- **Function:** `calc`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest /Users/krishna/SnAIproject/work/R25-T010/test_calculator.py -v --tb=short`

## Precondition Citations
- Line 33: `def calc(term):` accepts input expression
- Line 41: `term.replace(" ", "")` whitespace sanitization
- Line 42: `term.replace("^", "**")` exponent operator conversion
- Line 45: `term.replace("%", "/100.00")` percentage normalization
- Lines 50-62: `functions = [...]` anchor list of math functions
- Line 67: `eval(term)` expression evaluation

## Mutation Resistance Analysis
- **Target Invariant 1 (Power Operator):** `term.replace('^', '**')`
  - Mutant: `term.replace('^', '*')`
  - Input: `'2 ^ 3'`
  - Original Result: `8` (PASS)
  - Mutant Result: `6` (FAILS assertion `assert res == 8`)
- **Target Invariant 2 (Percentage Divisor):** `term.replace('%', '/100.00')`
  - Mutant: `term.replace('%', '/10.00')`
  - Input: `'50% * 100'`
  - Original Result: `50.0` (PASS)
  - Mutant Result: `500.0` (FAILS assertion `assert res == 50.0`)
- **Cleanliness Guarantee:** Production `calculator.py` contains no test-only hooks or mutant branches.

## Verification Matrix
| Scenario | Preconditions | Literal Input | Expected Output | Actual Result | Status |
|---|---|---|---|---|---|
| Smallest valid input | L33, L67 | `'0'` | `0` | `0` | PASS |
| Ordinary arithmetic input | L41, L67 | `'2 + 3 * 4'` | `14` | `14` | PASS |
| Exponentiation invariant | L42 | `'2 ^ 3'` | `8` | `8` | PASS |
| Percentage invariant | L45 | `'50% * 100'` | `50.0` | `50.0` | PASS |
| Scientific anchors | L50-62 | `'sin(0)'`, `'sqrt(16)'` | `0.0`, `4.0` | `0.0`, `4.0` | PASS |
| Exponent mutant detection | L42 | `'2 ^ 3'` on `*` mutant | Fails with `6 != 8` | Mutant detected | PASS |
| Percentage mutant detection | L45 | `'50% * 100'` on `/10` mutant | Fails with `500.0 != 50.0` | Mutant detected | PASS |

## Test Runner Output
```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.14/bin/python3
cachedir: .pytest_cache
rootdir: /Users/krishna/SnAIproject
collecting ... collected 7 items

work/R25-T010/test_calculator.py::TestCalculatorMutationResistance::test_smallest_valid_input_zero PASSED [ 14%]
work/R25-T010/test_calculator.py::TestCalculatorMutationResistance::test_ordinary_arithmetic_input PASSED [ 28%]
work/R25-T010/test_calculator.py::TestCalculatorMutationResistance::test_exponent_operator_invariant PASSED [ 42%]
work/R25-T010/test_calculator.py::TestCalculatorMutationResistance::test_percentage_normalization_invariant PASSED [ 57%]
work/R25-T010/test_calculator.py::TestCalculatorMutationResistance::test_math_functions_anchors PASSED [ 71%]
work/R25-T010/test_calculator.py::TestCalculatorMutationResistance::test_mutation_detection_exponent_mutant PASSED [ 85%]
work/R25-T010/test_calculator.py::TestCalculatorMutationResistance::test_mutation_detection_percentage_mutant PASSED [100%]

============================== 7 passed in 0.02s ===============================
```

**Exit Code:** 0
