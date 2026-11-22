## Description
This pull request adds mutation-resistant regression tests for `date_timeclient` in `date-timeclient.py`. It wraps the socket communication in a reusable function with an injectable socket factory for mock-based testing, documents preconditions citing source line anchors, proves mutation resistance against plausible single-line bugs (such as wrong destination port, altered formatting prefix, or reduced buffer capacity), and keeps the production code free of test hooks.

## Related Issue
Fixes: #24

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
- `date-timeclient.py`:
  - Structured socket operations into `date_timeclient(host=None, port=2905, socket_factory=None)` with guaranteed socket cleanup in a `finally` block.
  - Added docstring detailing preconditions citing lines 3, 4, 5, 6, and 7.
  - Guarded module-level execution with `if __name__ == '__main__':`.
- `work/R25-T020/test_datetimeclient.py`:
  - Tested smallest valid input (empty byte stream `b""`).
  - Tested ordinary input (standard timestamp string).
  - Proved mutation resistance: demonstrated that plausible mutants (connecting to port 2906, altering output prefix, or reducing `recv` buffer to 512) fail the named regression assertions.
- `work/R25-T020/check.py`: Automated test runner executing regression checks and generating verification receipts.
- `work/R25-T020/RESULTS.md`: Detailed test results matrix, mutation analysis, and precondition citations.

## Screenshots / Recordings
N/A - Network socket client logic and mutation-resistant unit tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T020/check.py
```
Output:
```
Ran 5 tests in 0.000s
OK
All R25-T020 checks passed successfully.
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
- Line 3: `soc = socket.socket(...)` socket initialization
- Line 4: `soc.connect((..., 2905))` connects to destination port 2905
- Line 5: `recmsg = soc.recv(1024)` reads up to 1024 bytes
- Line 6: `soc.close()` socket teardown
- Line 7: `"The time got from the server is %s" % recmsg.decode("ascii")` formatting normalization.
