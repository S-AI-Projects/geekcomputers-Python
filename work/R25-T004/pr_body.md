## Description
This pull request refactors `how to display the fibonacci sequence up to n-.py` into a reusable sequence generator `fibonacci_sequence(nterms)` (aliased as `how_to_display_the_fibonacci_sequence_up_to_n`), establishes contract documentation citing source lines, and validates the mathematical invariant $F(n+2) = F(n+1) + F(n)$ alongside specific fixture indices (0, 1, 2, 5, 10).

## Related Issue
Fixes: #9

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
- `how to display the fibonacci sequence up to n-.py`:
  - Encapsulated sequence generation logic inside `fibonacci_sequence` with alias `how_to_display_the_fibonacci_sequence_up_to_n`.
  - Added docstring citing base initial conditions and recurrence invariants.
  - Guarded interactive command-line loop in `main()` with `if __name__ == "__main__":`.
- `work/R25-T004/test_fibonacci.py`:
  - Tested fixture indices 0, 1, 2, 5, and 10 against expected values (0, 1, 1, 5, 55).
  - Verified property invariant $F(n+2) = F(n+1) + F(n)$ across the supported range.
  - Asserted zero and unit term boundaries (`nterms=0` -> `[]`, `nterms=1` -> `[0]`).
  - Implemented a deliberate recurrence mutant (`nth = n1 + n2 + 1`) to prove that invariant checks actively catch regressions.
- `work/R25-T004/check.py`: Focused automated test runner exporting verification results.
- `work/R25-T004/RESULTS.md`: Detailed test summary, source citations, and verification metrics.

## Screenshots / Recordings
N/A - CLI algorithm utility and property test suite.

## Testing
Executed local test runner:
```bash
python3 work/R25-T004/check.py
```
Output:
```
============================== 4 passed in 0.02s ===============================
All R25-T004 checks passed successfully.
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
- Line 6: Base sequence initialization `n1, n2 = 0, 1`
- Line 10: Input validation constraint `nterms <= 0`
- Line 17: Recurrence relation `nth = n1 + n2`
