## Description
This pull request adds invariant-based property tests for `Python Distance` in `Python Distance.py`. It formalizes the mathematical invariants governing power-of-two generation (length preservation, base value, bitwise equivalence, recurrence relation, and strict monotonicity) across 100 bounded test cases with a deterministic seed, documents the contract beside the implementation, and ensures clean module importability.

## Related Issue
Fixes: #18

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
- `Python Distance.py`:
  - Structured power-of-two calculation into `python_distance(terms=10)` with full backward compatibility.
  - Added docstring detailing mathematical invariants citing source line anchors.
  - Guarded interactive console print output with `if __name__ == '__main__':`.
- `work/R25-T014/test_python_distance.py`:
  - Tested smallest valid input (`terms=0` -> `[]`, `terms=1` -> `[1]`).
  - Tested ordinary input (`terms=10` -> `[1, 2, 4, 8, 16, 32, 64, 128, 256, 512]`).
  - Executed property test over 100 bounded cases (`terms in [0..60]`) with fixed deterministic random seed (seed=42).
  - Proved that deliberately breaking the recurrence invariant with a mutant (`2**x + 1`) is caught immediately.
- `work/R25-T014/check.py`: Automated test runner executing property checks and generating verification receipts.
- `work/R25-T014/RESULTS.md`: Detailed test results matrix, invariant specifications, and precondition citations.

## Screenshots / Recordings
N/A - Functional power mapping and property-based unit tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T014/check.py
```
Output:
```
Ran 5 tests in 0.001s
OK
All R25-T014 checks passed successfully.
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
- Line 3: `terms = 10` establishes default iteration terms fixture
- Line 9: `result = list(map(lambda x: 2**x, range(terms)))` defines the functional calculation.
