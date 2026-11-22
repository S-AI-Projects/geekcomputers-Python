## Description

Measures the scaling and complexity of `get_integer` and `addition` in `Sum of digits of a number.py`, isolates algorithm operations from process startup and I/O latency, verifies source anchors and independently calculated neighboring inputs, and adds complexity documentation and representative regression doctests.

## Related Issue

Fixes: #41

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] Tests (adding or updating tests)
- [x] Documentation update

## Changes Made

- **`Sum of digits of a number.py`**:
  - Documented algorithmic complexity of `get_integer` and `addition`, specifying the input size variable $d$ (number of decimal digits) and distinguishing worst-case claims ($O(d)$) from empirical observations.
  - Added dependency injection support `input_func=input` to `get_integer` preserving backwards compatibility.
  - Added a representative regression test `>>> addition(124) -> 7` derived from source anchor `>>> addition(123) -> 6`.
- **`work/R25-T039/test_sum_of_digits.py`**:
  - 13 focused tests covering source anchors (`addition(123) == 6`, `addition(-784) == 19`), independently derived neighbors (`addition(124) == 7`, `addition(-785) == 20`), `get_integer` correctness, retry/exhaustion semantics, doctest verification, and a 3-size, 5-repetition scaling experiment.
- **`work/R25-T039/check.py`**: Focused test runner exiting non-zero on any failure.
- **`work/R25-T039/timing_table.md` & `scaling_report.json`**: Timing measurements, median, and range across sizes $d \in \{100, 1000, 3000\}$.
- **`work/R25-T039/experiment_evidence.md`**: Complete experiment report, tool versions, and pre-change analysis.
- **`work/R25-T039/baseline.txt`**: Unaltered baseline copy before changes.

## Screenshots / Recordings

N/A – pure logic / algorithmic complexity experiment.

## Testing

Command executed:
```bash
python3 work/R25-T039/check.py
```
Output:
```
============================== 13 passed in 0.12s ==============================
```

Exit code: 0. 13 tests passed, 0 failed.

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

- Input size variable: $d$ = number of decimal digits in input string.
- Tested sizes: $d \in \{100, 1000, 3000\}$, 5 repetitions each with fixed PRNG seed 42.
- Correctness of all measured outputs was verified outside the timed interval.
- No pass/fail threshold depends on wall-clock speed.
