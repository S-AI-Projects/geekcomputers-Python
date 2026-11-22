## Description
This pull request modularizes `Randomnumber.py` into a callable function `random_number(start=0, end=9)` (aliased as `Randomnumber`), establishes explicit contract specifications, and validates output against an independent reference implementation under controlled pseudo-random number generator (PRNG) state.

## Related Issue
Fixes: #8

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
- `Randomnumber.py`:
  - Packaged script into `random_number(start=0, end=9)` with aliases `Randomnumber` and `randomnumber`.
  - Added docstring detailing preconditions, argument contracts, return types, and state side-effects.
  - Guarded top-level script execution in `main()` with `if __name__ == "__main__":`.
- `work/R25-T003/test_random_number.py`:
  - Built an independent reference generator using `random.Random.randrange`.
  - Verified smallest valid input (`start=0, end=0` returning `0` deterministically).
  - Verified ordinary input (`start=0, end=9` with fixed seed `42`).
  - Added seed-sweep cross-check comparing outputs across 50 independent seeds.
  - Asserted output shape, integer type constraints, and argument immutability.
- `work/R25-T003/check.py`: Automated test runner exporting test results and differential verification logs.
- `work/R25-T003/RESULTS.md`: Complete cross-check matrix, cited source preconditions, and environment records.

## Screenshots / Recordings
N/A - backend CLI script and differential unit tests.

## Testing
Executed local test runner:
```bash
python3 work/R25-T003/check.py
```
Output:
```
============================== 4 passed in 0.02s ===============================
All R25-T003 checks passed successfully.
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
- Line 4: `from random import randint`
- Line 6: Default interval bounds `randint(0, 9)`
