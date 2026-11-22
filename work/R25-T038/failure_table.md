# R25-T038 Failure Table

**Source file:** `Generate a random number between 0 to 9.py`

## Preconditions from Source

| Source Line | Statement | Precondition Established |
|-------------|-----------|--------------------------|
| Line 4 | `import random` | PRNG dependency available |
| Line 6 | `print(random.randint(0, 9))` | `start <= end`; returns `int` in `[start, end]` |

## Failure Branch

| Property | Value |
|----------|-------|
| Failure branch name | `inverted-range` |
| Source line | Line 6 – `random.randint(start, end)` delegates to `randrange(start, end+1)` which raises `ValueError` when `start > end` |
| Smallest reaching input | `start=1, end=0` |
| Expected behaviour | `ValueError` raised |
| Actual behaviour (before fix) | Script-level `print` with no way to inject `start/end`; no testable failure path |
| Actual behaviour (after refactor) | `generate_random_number(1, 0)` → `ValueError` ✅ |

## Fixture Table

| Test class | Input | Expected value | Source line |
|------------|-------|----------------|-------------|
| `TestSmallestValidInput::test_zero_range_returns_only_possible_value` | `start=0, end=0, rng=MockRng(0)` | `0` | Line 6 |
| `TestSmallestValidInput::test_zero_range_type_is_int` | `start=0, end=0, rng=MockRng(0)` | `isinstance(result, int) == True` | Line 6 |
| `TestSmallestValidInput::test_single_value_range_other_bound` | `start=5, end=5, rng=MockRng(5)` | `5` | Line 6 |
| `TestOrdinaryInput::test_returns_mocked_value_in_range` | `start=0, end=9, rng=MockRng(6)` | `6` | Line 6 |
| `TestOrdinaryInput::test_lower_bound_value` | `start=0, end=9, rng=MockRng(0)` | `0` | Line 6 |
| `TestOrdinaryInput::test_upper_bound_value` | `start=0, end=9, rng=MockRng(9)` | `9` | Line 6 |
| `TestOrdinaryInput::test_arbitrary_range_mid_value` | `start=3, end=7, rng=MockRng(5)` | `5` | Line 6 |
| `TestOrdinaryInput::test_default_params_use_real_rng` | `start=0, end=9` (live rng) | `0 <= result <= 9` | Line 6 |
| `TestFailurePath::test_inverted_range_raises_value_error` | `start=1, end=0` | `ValueError` | Line 6 |
| `TestFailurePath::test_large_inverted_range_raises_value_error` | `start=10, end=5` | `ValueError` | Line 6 |
| `TestFailurePath::test_negative_inverted_range_raises_value_error` | `start=-1, end=-5` | `ValueError` | Line 6 |
| `TestPostFailureRecovery::test_valid_call_after_value_error` | `start=5, end=2` → error; then `start=0, end=9, rng=MockRng(7)` | `7` | Lines 4 & 6 |
| `TestPostFailureRecovery::test_multiple_valid_calls_after_failure` | 3× error; then `start=2, end=4, rng=MockRng(3)` | `3` | Lines 4 & 6 |
| `TestOutputFormat::test_output_is_integer_string` | mock value `4` | `'4'` (string) | Line 6 |
| `TestOutputFormat::test_output_is_parseable_as_int` | mock value `9` | `int(output) == 9` | Line 6 |
| `TestOutputFormat::test_output_newline_terminated` | `start=0, end=9, rng=MockRng(3)` | raw output ends with `\n` | Line 6 |
