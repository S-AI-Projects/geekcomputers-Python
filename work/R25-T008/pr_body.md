## Description
This pull request covers the documented failure behavior of `main` in `calc_area.py`. When a user provides a shape selection outside the valid range [1, 7], the function enters the fallback `else:` branch at source line 32 and outputs "You have selected wrong choice." without raising uncaught exceptions. The PR also allows dependency injection for console I/O to enable clean, isolated testing and verifies that valid area calculations continue to succeed after encountering a failure input.

## Related Issue
Fixes: #13

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
- `calc_area.py`:
  - Updated `main(input_fn=None, print_fn=None)` with default parameters preserving existing CLI usage while allowing deterministic test mocking.
  - Documented preconditions, supported inputs, and the failure fallback branch at line 32.
  - Guarded top-level script execution in `if __name__ == "__main__":`.
- `work/R25-T008/test_calc_area.py`:
  - Tested documented failure branch (shape=9) asserting `"You have selected wrong choice."`.
  - Tested smallest valid input (square with side=0.0) asserting `"Area of square = 0.0"`.
  - Tested ordinary input (square with side=5.0) asserting `"Area of square = 25.0"`.
  - Verified state integrity by running an ordinary calculation immediately following a failure input.
- `work/R25-T008/check.py`: Automated test runner exporting test results.
- `work/R25-T008/RESULTS.md`: Complete verification report and precondition citations.

## Screenshots / Recordings
N/A - CLI area calculation utility and unit tests.

## Testing
Executed local test runner:
```bash
python3 work/R25-T008/check.py
```
Output:
```
============================== 4 passed in 0.02s ===============================
All R25-T008 checks passed successfully.
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
- Line 5: `shape = int(...)` choice input
- Line 11: `shape == 1` square area formula
- Line 14: `shape == 2` rectangle area formula
- Line 32: `else: print("You have selected wrong choice.")` failure fallback branch
- Line 35: `restart = input(...)` loop control
