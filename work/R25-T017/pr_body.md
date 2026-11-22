## Description
This pull request adds executable documentation and regression tests for `print_rangoli` in `rangoli.py`. It enriches the docstring with a concrete worked example, explains the decisive state transition governing hyphen suppression and Python's string-centering symmetry mechanics, and adds unit tests that execute the documentation example and verify intermediate and final outputs.

## Related Issue
Fixes: #21

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
- `rangoli.py`:
  - Enriched `print_rangoli` docstring with preconditions, worked input/output examples (`n=1` and `n=3`), and an explanation of the decisive state transition at `len(string) == width`.
- `work/R25-T017/test_rangoli.py`:
  - Executed smallest valid input (`n=1` -> `"a"`).
  - Executed ordinary input (`n=3` -> 5-line symmetric alphabet pattern).
  - Verified the decisive state transition and `str.center` padding arithmetic in isolation.
- `work/R25-T017/check.py`: Automated test runner executing regression checks and generating verification receipts.
- `work/R25-T017/RESULTS.md`: Detailed test results matrix and precondition citations.

## Screenshots / Recordings
N/A - ASCII Rangoli pattern generator and executable documentation tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T017/check.py
```
Output:
```
Ran 3 tests in 0.000s
OK
All R25-T017 checks passed successfully.
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
- Line 5: `def print_rangoli(n):` input size parameter
- Line 7: `width = 4 * n - 3` calculates total line width
- Line 14: Decreasing alphabet characters `chr(96 + n - j)`
- Line 19: Increasing alphabet characters `chr(97 + n - k)`
- Lines 24, 38: `string.center(width, "-")` centered line rendering.
