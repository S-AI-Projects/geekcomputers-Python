## Description

This PR implements task R25-T037 for `simple_calculator.py`. It adds an executable worked example to `add` explaining the calculation from input through intermediate state to the final result, identifying the decisive state transition (the binary operator evaluation `x + y`), and adds a focused test suite validating the executable documentation, source anchors, derived neighbors, and CLI integration.

## Related Issue

Fixes: #39

## Type of Change

- [x] Documentation
- [x] Tests

## Changes Made

- **`simple_calculator.py`**:
  - Enhanced the docstring of `add` with contract/preconditions, explanation of the decisive state transition, and executable doctest examples.
  - Documented preconditions citing source lines 18 and 20.
  - Preserved original public interface, function signatures, and behavior.
- **`work/R25-T037/test_calculator_example.py`**:
  - Doctest execution test validating module and function doctests via `doctest.testmod` (8/8 doctests passing).
  - Source anchor tests: `add(2, 3) -> 5`, `subtract(10, 4) -> 6`, `multiply(3, 4) -> 12`, `divide(8, 2) -> 4.0`.
  - Derived neighboring supported inputs: `add(3, 4) -> 7`, `add(2.5, 3.5) -> 6.0`, `add(0, 0) -> 0`, `add(-5, 5) -> 0`, `add(10, -3) -> 7`.
  - Traced execution tests verifying intermediate states and decisive state transition for integer and float addition.
  - Function purity and idempotence tests.
  - Interactive CLI test verifying `calculator()` with mocked `input` executing option 1 (`add`).
- **`work/R25-T037/check.py`**:
  - Focused test runner executing pytest and recording evidence in `results.txt`.
- **`work/R25-T037/baseline.txt`**:
  - Baseline analysis recording environment, observable dependencies, source line citations, hand calculations, and state transition analysis.
- **`work/R25-T037/example_table.md`**:
  - Preconditions, decisive state transition diagram, and fixture matrix.
- **`work/R25-T037/results.txt`**:
  - Test execution results (15 passed in 0.07s).

## Screenshots / Recordings

N/A — command-line utility.

## Testing

Tested locally using Python 3.12.16 and pytest 9.2.0:

```bash
source .venv/bin/activate
python3 work/R25-T037/check.py
```

Result:
```
============================== 15 passed in 0.07s ==============================
All R25-T037 checks PASSED.
Exit code: 0
```

Doctest execution verification:
```bash
python3 -m doctest simple_calculator.py -v
# 8 tests in 2 items.
# 8 passed and 0 failed.
# Test passed.
```

## Checklist

- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes

- The decisive state transition identified is the evaluation of the binary addition expression `x + y`: transitioning two distinct operand input bindings into a single synthesized scalar sum.
- All docstring examples use real public names and valid imports.
- Preconditions from source lines 8, 10, 12, 14, 18, 20, and 43 are cited in tests and documentation.
