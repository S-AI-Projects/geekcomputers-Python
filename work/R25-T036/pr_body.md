## Description

This PR implements task R25-T036 for `gcd.py`. It refactors one coherent calculation in `gcd`: extracting the common divisor divisibility check (`a % i == 0 and b % i == 0`) into an explicit, intention-revealing helper function `is_common_divisor(i, a, b)`, and encapsulating the linear search in `gcd(a, b)` while preserving original algorithm, ordering, return types, and CLI behavior under `if __name__ == "__main__":`.

## Related Issue

Fixes: #38

## Type of Change

- [x] Refactoring / Maintenance
- [x] Tests
- [x] Documentation

## Changes Made

- **`gcd.py`**:
  - Extracted common divisor check into `is_common_divisor(i, a, b)` returning boolean divisibility without altering algorithm.
  - Encapsulated linear search in `gcd(a, b)` returning greatest common divisor (or `-1` if no positive divisor exists).
  - Guarded interactive user inputs under `if __name__ == "__main__":` to preserve CLI behavior while allowing clean module import.
  - Documented contract, preconditions, and source line citations (lines 6, 7, 9, 10, 11, 12, 13, 14, 16).
- **`work/R25-T036/test_gcd.py`**:
  - Task fixture assertions: `(54, 24) -> 6`, `(17, 13) -> 1`, `(9, 9) -> 9`.
  - Zero argument behavior: `(0, 5) -> -1`, `(5, 0) -> -1`, `(0, 0) -> -1` verifying sentinel `-1` preservation when loop condition `1 <= 0` fails immediately.
  - Before/After equivalence tests across multiple inputs comparing refactored implementation directly against original while loop.
  - Helper unit tests for `is_common_divisor`.
  - CLI format string preservation tests.
- **`work/R25-T036/check.py`**:
  - Focused test runner executing pytest and recording results.
- **`work/R25-T036/baseline.txt`**:
  - Analysis recording public inputs, return contracts, mutation behavior, source citations, and refactoring plan.
- **`work/R25-T036/refactor_table.md`**:
  - Detailed refactoring analysis and fixture matrix.
- **`work/R25-T036/results.txt`**:
  - Test execution results (17 passed in 0.03s).

## Screenshots / Recordings

N/A — command-line utility.

## Testing

Tested locally using Python 3.12.16 and pytest 9.2.0:

```bash
source .venv/bin/activate
python3 work/R25-T036/check.py
```

Result:
```
============================== 17 passed in 0.03s ==============================
All R25-T036 checks PASSED.
Exit code: 0
```

## Checklist

- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes

- The particular operation made clearer is candidate common divisor verification (`is_common_divisor`), separating the arithmetic divisibility predicate from loop traversal and accumulator state.
- The before and after implementations agree completely across all tested cases.
- Preconditions from source lines 6, 7, 9, 10, 11, 12, 13, 14, and 16 are cited in docstrings and tests.
