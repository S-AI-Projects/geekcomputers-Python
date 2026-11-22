## Description

Refactors `automail.py` into a testable `automail(recThreads=None, client=None, single_pass=True)` function with dependency injection, adds regression tests for the smallest valid input and ordinary inputs with source-line citations, and proves mutation resistance against plausible one-line mistakes in boundary conditions and string accumulation.

## Related Issue

Fixes: #42

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] Tests (adding or updating tests)
- [x] Documentation update

## Changes Made

- **`automail.py`**:
  - Packaged continuous polling script into `automail(recThreads=None, client=None, single_pass=True)` function.
  - Guarded top-level CLI execution under `if __name__ == "__main__":` to eliminate import side effects and allow isolated testing.
  - Added full docstrings citing source lines for all preconditions.
  - Kept production implementation 100% clean with no mutations or test-only branches.
- **`work/R25-T040/test_automail.py`**:
  - Implemented 8 comprehensive tests covering smallest valid input (`"Simon says:"`), ordinary input (`"Simon says: check server status"`), `ENDTASK` termination, and mutation resistance.
  - Proved that the regression suite detects:
    1. Accumulation mutant (`replyContent = "I am now doing" + " ".join(subEval)`) via `test_accumulation_invariant_ordinary_input`.
    2. Off-by-one boundary mutant (`len(subEval) > 2`) via `test_boundary_invariant_smallest_input`.
- **`work/R25-T040/check.py`**: Focused test runner exiting non-zero on failure.
- **`work/R25-T040/mutation_report.md`**: Full mutation and fixture report citing baseline lines and differential proofs.
- **`work/R25-T040/baseline.txt`**: Unaltered baseline copy before changes.

## Screenshots / Recordings

N/A – backend email automation script and test suite.

## Testing

Command executed:
```bash
python3 work/R25-T040/check.py
```
Output:
```
============================== 8 passed in 0.03s ===============================
```

Exit code: 0. 8 tests passed, 0 failed.

## Checklist

- [x] My code follows the style guidelines of this project
- [x] I have performed a self-review of my code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] I have made corresponding changes to the documentation
- [x] My changes generate no new warnings
- [x] I have added tests that prove my fix is effective or that my feature works
- [x] New and existing unit tests pass locally with my changes
- [x] Any dependent changes have been merged and published in downstream modules

## Additional Notes

- Precondition citations from baseline: Line 11 (threads iterable), Line 14 (split subject), Line 15 (sender pattern), Line 16 (command trigger), Line 23 (reply accumulation), Line 24 (send response), Line 25 (trash thread), Line 26 (kill command).
- Mutants were evaluated exclusively within the test suite and excluded from `automail.py`.
