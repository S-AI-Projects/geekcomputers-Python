## Description

Refactors `Generate a random number between 0 to 9.py` to expose a testable `generate_random_number(start, end, rng)` function with dependency injection, then adds a full failure-path test suite covering smallest valid input, ordinary inputs, the `ValueError` failure branch (`start > end`), post-failure recovery, and CLI output format.

## Related Issue

Fixes: #40

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] Tests (adding or updating tests)
- [ ] Documentation update

## Changes Made

- **`Generate a random number between 0 to 9.py`**: Extracted `generate_random_number(start=0, end=9, rng=None)` with dependency-injected RNG; guarded CLI print under `if __name__ == "__main__":`.
- **`work/R25-T038/test_random_number.py`**: 16 deterministic tests across 5 classes:
  - `TestSmallestValidInput` – degenerate range `start=end=0`
  - `TestOrdinaryInput` – mocked values across valid range
  - `TestFailurePath` – `start > end` → `ValueError` (source: line 6)
  - `TestPostFailureRecovery` – valid calls succeed after failure
  - `TestOutputFormat` – CLI stdout correctness
- **`work/R25-T038/check.py`**: Focused test runner; exits non-zero on failure.
- **`work/R25-T038/failure_table.md`**: Documents each precondition, failure branch, and fixture with source-line citations.
- **`work/R25-T038/baseline.txt`**: Original source captured before changes.

## Screenshots / Recordings

N/A – pure logic, no UI.

## Testing

```
python3 work/R25-T038/check.py
# 16 passed in 0.03s
```

All 16 tests pass. Exit code 0.

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

- Smallest failing input reaching the `ValueError` branch: `start=1, end=0`.
- All tests use a `_MockRng` stub for deterministic assertions; no live randomness.
- Original defaults (`start=0, end=9`) are preserved; existing CLI behaviour unchanged.
