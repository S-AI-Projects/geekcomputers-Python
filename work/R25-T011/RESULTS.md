# Verification Evidence — R25-T011

## Target
- **Script:** four_digit_num_combination.py
- **Function:** `four_digit_combinations`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m unittest /Users/nevilmaru009/.gemini/antigravity/scratch/geekcomputers-Python/work/R25-T011/test_four_digit_num_combination.py -v`

## Precondition Citations
- Line 7: `numbers = []` establishes the default accumulation list fixture.
- Line 8: `range(limit)` specifies iteration boundaries.
- Line 9: `code = str(code).zfill(4)` zero-pads integers to 4 characters.
- Line 10: `print(code)` outputs each code to stdout.
- Line 11: `numbers.append(code)` mutates the accumulation list in-place.

## Contract Summary
- **Input/Output Contract:** Documented explicit parameter types, limits, and return values.
- **Separation of Concerns:** Returned list verified independently from observable in-place mutation of the `numbers` fixture.
- **Side Effects Mocked:** Standard output captured with `io.StringIO` during unit test execution.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input | L7, L8, L9, L10 | `limit=1` | `['0000']` | `['0000']` | PASS |
| Ordinary input | L7, L8, L9, L10 | `limit=5` | `['0000', '0001', '0002', '0003', '0004']` | `['0000', '0001', '0002', '0003', '0004']` | PASS |
| Observable mutation | L7, L11 | `limit=3, numbers=[]` | `numbers == ['0000', '0001', '0002']` | `numbers == ['0000', '0001', '0002']` | PASS |
| Boundary: zero limit | L8 | `limit=0` | `[]` | `[]` | PASS |
| Boundary: padding transition | L9 | `limit=11` | `result[9]=='0009', result[10]=='0010'` | `result[9]=='0009', result[10]=='0010'` | PASS |

## Test Runner Output
```
test_boundary_padding_transition (work.R25-T011.test_four_digit_num_combination.TestFourDigitCombinationsContract.test_boundary_padding_transition)
Domain boundary: zero-padding transition from 1-digit to 2-digit numbers. ... ok
test_boundary_zero_limit (work.R25-T011.test_four_digit_num_combination.TestFourDigitCombinationsContract.test_boundary_zero_limit)
Smallest supported boundary: limit=0 (empty execution). ... ok
test_observable_mutation_separate_from_return (work.R25-T011.test_four_digit_num_combination.TestFourDigitCombinationsContract.test_observable_mutation_separate_from_return)
Separate test for observable mutation on passed list fixture. ... ok
test_ordinary_input (work.R25-T011.test_four_digit_num_combination.TestFourDigitCombinationsContract.test_ordinary_input)
Ordinary input: limit=5. ... ok
test_smallest_valid_input (work.R25-T011.test_four_digit_num_combination.TestFourDigitCombinationsContract.test_smallest_valid_input)
Smallest valid input: limit=1. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

**Exit Code:** 0
