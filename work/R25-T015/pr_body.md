## Description
This pull request ensures deterministic execution, dependency isolation, and repeatability for `draw_diamond` in `diamond.py`. It introduces a non-breaking dependency seam (`output_fn=print`) for deterministic output capture without coupling tests to global standard output, proves input isolation across consecutive runs, and wraps CLI `input()` invocation under `if __name__ == '__main__':` for clean importability.

## Related Issue
Fixes: #19

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
- `diamond.py`:
  - Added optional dependency injection parameter `output_fn=print` with default preserving existing callers.
  - Documented preconditions, parity requirements, and deterministic properties in docstrings.
  - Guarded interactive `input()` and execution under `if __name__ == '__main__':`.
- `work/R25-T015/test_diamond.py`:
  - Tested smallest valid input (`n=1` -> single asterisk `["*"]`).
  - Tested ordinary input (`n=3` -> 3-line diamond, `n=5` -> 5-line diamond).
  - Tested non-odd input rejection (`n=4`).
  - Verified repeatability and input isolation by asserting that an intervening run (`n=7`) cannot alter subsequent results for `n=3`.
- `work/R25-T015/check.py`: Automated test runner executing repeatability checks and generating verification receipts.
- `work/R25-T015/RESULTS.md`: Detailed test results matrix and precondition citations.

## Screenshots / Recordings
N/A - ASCII diamond generation and repeatability unit tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T015/check.py
```
Output:
```
Ran 5 tests in 0.000s
OK
All R25-T015 checks passed successfully.
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
- Line 1: `def draw_diamond(n):` input interface with dependency seam
- Line 2: `if n % 2 != 0:` parity check (odd number requirement)
- Lines 4-5: Upper pyramid expansion step
- Lines 9-10: Lower inverted pyramid contraction step
- Line 14: Non-odd rejection fallback.
