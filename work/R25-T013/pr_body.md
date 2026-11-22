## Description
This pull request adds reference-comparison regression tests for `print_all` in `ex20.py`. It compares `print_all` against an independent stream-processing oracle across 21 distinct valid inputs (including boundary cases, empty streams, single characters, multiline strings, unicode, and symbols), verifies stream pointer mutation to EOF, and guards command-line execution under `if __name__ == '__main__':` to allow clean test importing.

## Related Issue
Fixes: #17

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
- `ex20.py`:
  - Added docstring to `print_all` citing source precondition anchors and documenting a representative input/output result.
  - Wrapped global argument parsing and script execution in `main()` with `if __name__ == '__main__':` guard so the module can be imported cleanly.
- `work/R25-T013/test_ex20.py`:
  - Implemented an independent reference oracle using `readline()` chunked accumulation without invoking the target under test.
  - Tested smallest valid input (`io.StringIO("")`).
  - Tested ordinary multiline input.
  - Verified stream pointer mutation from 0 to EOF.
  - Evaluated 21 diverse input cases comparing target output and stream mutation against the independent oracle.
- `work/R25-T013/check.py`: Automated test runner executing regression checks and generating verification receipts.
- `work/R25-T013/RESULTS.md`: Detailed test results matrix, oracle specification, and precondition citations.

## Screenshots / Recordings
N/A - File stream reading logic and unit tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T013/check.py
```
Output:
```
Ran 4 tests in 0.001s
OK
All R25-T013 checks passed successfully.
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
- Line 6: `def print_all(f):` establishes stream input interface
- Line 7: `print(f.read())` reads stream to EOF and emits to stdout
- Line 10: `f.seek(0)` establishes stream pointer and mutation awareness.
