## Description
This pull request measures the algorithmic work and scaling behavior of `sid2user` in `recyclebin.py`. It adds explicit complexity documentation (identifying the input size variable $n$ as the length of the resolved path), injects registry dependencies for isolated testing on non-Windows platforms, and verifies correctness and operation counts across varying input scales without relying on wall-clock timing thresholds.

## Related Issue
Fixes: #14

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
- `recyclebin.py`:
  - Updated `sid2user(sid, key_opener=None, value_querier=None)` to allow dependency injection while preserving default Windows registry lookups.
  - Added docstring detailing asymptotic complexity ($O(n)$ string splitting) and source citations.
  - Guarded platform-specific `winreg` imports to ensure clean importing in cross-platform CI environments.
- `work/R25-T009/test_recyclebin.py`:
  - Tested smallest valid input (`'S-1-0-0'` -> `'Nobody'`).
  - Tested ordinary input (Domain Admin SID -> `'Administrator'`).
  - Verified exception fallback returning raw input string on missing registry entries.
  - Measured algorithmic scaling across path lengths up to 20,000 characters, validating $O(1)$ registry calls and accurate output at every scale without wall-clock dependencies.
- `work/R25-T009/check.py`: Automated test runner exporting scaling and verification evidence.
- `work/R25-T009/RESULTS.md`: Detailed complexity statement, source citations, and test matrix.

## Screenshots / Recordings
N/A - Windows registry SID resolution logic and algorithmic scaling tests.

## Testing
Executed local test runner:
```bash
python3 work/R25-T009/check.py
```
Output:
```
============================== 4 passed in 0.02s ===============================
All R25-T009 checks passed successfully.
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
- Line 20: `sid2user(sid)` acceptance of string SID
- Line 21: Registry subkey path concatenation
- Line 25: `ProfileImagePath` value query
- Line 26: String split on `'\\'` selecting the trailing segment
- Line 28: Fallback on exception returning original `sid`
- Line 32: Anchor `dirs = ["c:\\Recycler\\", "C:\\Recycled\\", "C:\\$RECYCLE.BIN\\"]`
