# R25-T059 — Measure the work done by angle_type()

## Objective

Check the correctness of `angle_type()` and measure its observed work
across increasing batches of repeated calls.

## Source inspection and line anchors

File: `Type_of_angles_of_triangle.py`

- Line 5: defines `angle_type()` with no parameters.
- Line 6: initializes `angles = []`.
- Lines 8–12: defines the fixed classification dictionary.
- Lines 18, 30, 42: reads the three angles.
- Lines 20–26, 32–38, 44–50: validates and appends the angles.
- Line 54: calculates the sum of the three angles.
- Lines 55–57: rejects a total other than 180 and returns `-1`.
- Lines 61–68: classifies right, acute, and obtuse triangles.
- Line 71 onward: invokes the function at module level.

The source was not modified.

## Correctness tests

### Smallest valid input

Literal input:

    60, 60, 60

Independent calculation:

    60 + 60 + 60 = 180

All three angles are less than 90 degrees.

Expected classification:

    Acute Angle Triangle

Actual result: passed.

### Ordinary valid input

Literal input:

    30, 60, 90

Independent calculation:

    30 + 60 + 90 = 180

One angle is exactly 90 degrees.

Expected classification:

    Right Angle Triangle

Actual result: passed.

### Invalid angle sum

Literal input:

    60, 60, 30

Independent calculation:

    60 + 60 + 30 = 150

This reaches the invalid-sum branch at source lines 55–57.

Expected return value:

    -1

Expected error message:

    It is not a triangle!Please enter valid angles.

Actual result: passed.

## Benchmark methodology

The function accepts no arguments and always reads exactly three angles.
Its input size does not increase between calls.

For measurement, the benchmark repeats independent calls using fresh
mocked input values of 60, 60, and 60.

Batch sizes:

    100, 500, 1000 calls

Repetitions:

    5 per batch size

Measurement details:

- Uses `time.perf_counter_ns()`.
- Reports median and minimum-to-maximum range per call.
- Imports the module before timing.
- Excludes process startup and real terminal I/O.
- Mocks input and print during each timed batch.
- Mocked function-call overhead and the result assertion remain included.
- No timing threshold is used as a pass/fail condition.

## Actual benchmark results

Command:

    python3 work/R25-T059/benchmark.py

Observed results:

| Calls per batch | Median (ns/call) | Range (ns/call) |
|---:|---:|---:|
| 100 | 931.7 | 920.0–982.1 |
| 500 | 924.1 | 917.8–933.6 |
| 1000 | 946.5 | 939.0–956.5 |

These are measurements from this environment, not guaranteed performance
figures. The similar per-call observations across batch sizes are consistent
with a fixed amount of work per invocation.

## Complexity interpretation

Let n be the number of angles processed by one invocation.

The implementation always reads and processes exactly three angles.
Therefore n is fixed at 3, and the work per invocation is O(1) with
respect to the number of angles.

The benchmark batch size B is the number of repeated invocations, not
the function's input size. Running B calls performs O(B) total work.
The benchmark does not establish scaling for a variable-length angle list,
because the public function does not accept one.

## Test isolation

The tests import only the named target module and mock input.
The source's top-level demonstration call is supplied with controlled
input during import. Its output is discarded before each explicit test call.

## Verification

Focused test command:

    python3 -m pytest work/R25-T059/test_angle_type.py -q

Required runner command:

    python3 work/R25-T059/check.py

Actual required runner result:

    3 passed in 0.06s

Environment:

- Python 3.12.16
- pytest 9.2.0

## Deliverables

- `test_angle_type.py` — correctness and invalid-sum tests
- `benchmark.py` — repeatable benchmark
- `check.py` — focused test runner
- `RESULTS.md` — source anchors, test evidence, measurements, and complexity interpretation
