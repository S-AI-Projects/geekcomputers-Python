## Description
This pull request modularizes `Decimal number to binary function.py` by introducing `decimal_to_binary(number)` alongside explicit contract documentation and unit tests for domain boundaries. It explicitly characterizes supported boundaries (including zero, positive units, negative units, numeric string coercion, and powers of two), cites source preconditions, and isolates interactive CLI prompts behind `main()`.

## Related Issue
Fixes: #7

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
- `Decimal number to binary function.py`:
  - Defined `decimal_to_binary` (with alias `decimal_number_to_binary_function`) encapsulating `bin(int(number))` with a contract docstring.
  - Guarded interactive terminal inputs in `main()` behind `if __name__ == "__main__":`.
- `work/R25-T002/test_decimal_to_binary.py`:
  - Added boundary tests verifying smallest valid input (`0` -> `'0b0'`), ordinary input (`10` -> `'0b1010'`), unit boundary (`1` -> `'0b1'`), negative unit (`-1` -> `'-0b1'`), negative ordinary (`-10` -> `'-0b1010'`), string coercion (`'42'` -> `'0b101010'`), and large powers of two (`1024` -> `'0b10000000000'`).
- `work/R25-T002/check.py`: Implemented automated test runner capturing boundary table evidence and execution logs.
- `work/R25-T002/RESULTS.md`: Documented boundary test matrix, precondition citations, and environment details.

## Screenshots / Recordings
N/A - CLI conversion utility and unit tests.

## Testing
Executed local test runner:
```bash
python3 work/R25-T002/check.py
```
Output:
```
============================== 7 passed in 0.02s ===============================
All R25-T002 checks passed successfully.
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
- Line 2: `int(...)` input conversion precondition
- Line 5: `bin(number)` conversion producing standard `'0b'` prefix
