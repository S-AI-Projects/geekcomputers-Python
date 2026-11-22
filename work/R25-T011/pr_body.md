## Description
This pull request locks down the input/output contract and regression behavior of `four_digit_combinations` in `four_digit_num_combination.py`. It adds explicit contract documentation citing source precondition anchors, enables repeatable fixture testing, separates return values from in-place list mutation checks, and preserves 100% backward compatibility for zero-argument invocation.

## Related Issue
Fixes: #2

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
- `four_digit_num_combination.py`:
  - Added comprehensive docstring documenting preconditions, parameter boundaries, return values, and side-effects.
  - Added optional `limit` and `numbers` parameters with default values (`limit=10000, numbers=None`) to enable testing while keeping default behavior identical.
- `work/R25-T011/test_four_digit_num_combination.py`:
  - Added regression test for smallest valid input (`limit=1` -> `['0000']`).
  - Added regression test for ordinary input (`limit=5` -> `['0000', '0001', '0002', '0003', '0004']`).
  - Separately asserted observable mutation of passed `numbers` fixture vs returned value.
  - Covered boundary condition for `limit=0` and zero-padding domain transitions across decade boundaries (`0009` to `0010`).
  - Mocked standard output cleanly using `io.StringIO`.
- `work/R25-T011/check.py`: Automated test runner executing regression checks and generating verification receipts.
- `work/R25-T011/RESULTS.md`: Detailed test results matrix and precondition citations.

## Screenshots / Recordings
N/A - Numerical combinations logic and unit tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T011/check.py
```
Output:
```
Ran 5 tests in 0.000s
OK
All R25-T011 checks passed successfully.
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
- Line 7: `numbers = []` establishes accumulation fixture.
- Line 8: `range(limit)` specifies iteration boundaries.
- Line 9: `code = str(code).zfill(4)` zero-pads integers to 4 characters.
- Line 10: `print(code)` outputs each code to stdout.
- Line 11: `numbers.append(code)` mutates the accumulation list in-place.
