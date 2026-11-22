## Description
This pull request strengthens the test suite for `calc` in `calculator.py` by proving mutation resistance against plausible single-line bugs in arithmetic string normalization (such as accidental single-asterisk multiplication instead of exponentiation, or incorrect percentage division scale). It also documents the contract, ensures `math` functions are properly scoped, safely handles `raw_input`, and keeps the production code free of mutation artifacts.

## Related Issue
Fixes: #15

## Type of Change
- [ ] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [x] Refactoring / Maintenance
- [ ] CI/CD

## Changes Made
- `calculator.py`:
  - Added docstring detailing preconditions, supported syntax normalization rules, and error fallbacks.
  - Ensured `math` is imported and `raw_input` does not trigger interactive file prompts during import.
  - Kept production implementation clean with zero test hooks or mutant branches.
- `work/R25-T010/test_calculator.py`:
  - Tested smallest valid input (`"0"` -> `0`) and ordinary input (`"2 + 3 * 4"` -> `14`).
  - Added invariant tests for exponentiation (`"2 ^ 3"` -> `8`) and percentage normalization (`"50% * 100"` -> `50.0`).
  - Tested math function anchors (`sin`, `sqrt`, `pi`).
  - Proved mutation resistance: demonstrated that plausible one-line bugs in exponentiation and percentage normalization are caught by the regression assertions.
- `work/R25-T010/check.py`: Automated test runner producing execution receipts.
- `work/R25-T010/RESULTS.md`: Detailed test matrix, mutation analysis, and precondition citations.

## Screenshots / Recordings
N/A - scientific calculator parsing logic and mutation-resistant unit tests.

## Testing
Executed local test runner:
```bash
python3 work/R25-T010/check.py
```
Output:
```
============================== 7 passed in 0.02s ===============================
All R25-T010 checks passed successfully.
```
Exit code: 0.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Preconditions cited directly from source lines:
- Line 33: `def calc(term):` accepts mathematical string
- Line 41: `term.replace(" ", "")` whitespace sanitization
- Line 42: `term.replace("^", "**")` exponent operator conversion
- Line 45: `term.replace("%", "/100.00")` percentage normalization
- Lines 50-62: `functions = [...]` anchor list of math functions
- Line 67: `eval(term)` expression evaluation
