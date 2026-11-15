# R25-T058 — Swapper failure behavior

## Objective

Test the documented failure behavior of `Swapper` in `swap.py`,
and verify that an existing valid instance remains usable after failure.

## Source inspection and line anchors

- Line 18: `Swapper.__init__(self, x, y)` public constructor.
- Line 30: validates that both arguments are integers or floats.
- Line 31: raises `ValueError` when validation fails.
- Lines 33–34: assigns `self.x` and `self.y` only after validation.
- Line 45: swaps the values using tuple unpacking.
- Lines 44 and 46: display values before and after swapping.

No implementation changes were necessary. The original `swap.py`
was left unchanged.

## Test cases

### 1. Smallest invalid input

Input:

    Swapper("a", 0)

Expected:

    ValueError("Both x and y should be integers.")

Actual:

    ValueError raised with the expected message.

The input reaches the validation and exception branch at lines 30–31.
The instance attribute assignments at lines 33–34 are not reached.

### 2. Ordinary invalid input

Input:

    Swapper(5, "invalid")

Expected:

    ValueError("Both x and y should be integers.")

Actual:

    ValueError raised with the expected message.

This also exercises the constructor validation branch at lines 30–31.

### 3. Valid object after failed construction

Initial valid input:

    Swapper(5, 10)

Expected initial state:

    x = 5
    y = 10

After a separate invalid construction attempt:

    Swapper("a", 0)

Expected existing-object state:

    x = 5
    y = 10

Actual:

    x = 5
    y = 10

Then call:

    instance.swap_tuple_unpacking()

Expected final state:

    x = 10
    y = 5

Actual final state:

    x = 10
    y = 5

Expected printed output:

    Before swapping x: 5, y: 10
    After swapping x: 10, y: 5

Actual printed output matched exactly.

The swap is performed at source line 45.

## Test isolation

The test imports only `swap.py`.
Its top-level demonstration output is suppressed during import.
The original print function is restored for the behavior tests.
No external I/O is required.

## Verification

Focused test command:

    python3 -m pytest work/R25-T058/test_swapper.py -q

Result:

    3 passed in 0.07s

Required runner command:

    python3 work/R25-T058/check.py

Result:

    3 passed in 0.10s

## Environment

- Python 3.12.16
- pytest 9.2.0

## Deliverables

- `test_swapper.py` — focused failure and recovery tests
- `check.py` — repeatable test runner
- `RESULTS.md` — source anchors, inputs, expected and actual results
