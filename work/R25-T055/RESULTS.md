# T055 — Repeatable verification of `get_operator_fn`

## Objective

Verify that `get_operator_fn` returns repeatable operator behavior and that separate calls do not interfere with one another.

## Source inspection

File: `Voice Command Calculator.py`

- Lines 15–29: `get_operator_fn` maps operator strings to functions from Python's `operator` module.
- Line 33: `eval_binary_expr` converts both operands to integers before evaluating the operation.
- Line 37: the module invokes speech recognition at import time.

The original source file was not modified.

## Test isolation

The tests mock the `speech_recognition` module, microphone, recognizer, and `print` during module import. No physical microphone or Google speech-recognition network request is required.

## Test cases

| Test | Inputs | Expected result |
|---|---|---:|
| Smallest valid addition | `0 + 0` | `0` |
| Ordinary multiplication | `7 x 3` | `21` |
| Repeated addition lookup | `4 + 5` | `9` |

The tests also verify repeated calls, equivalent behavior from repeated operator lookups, and that input values remain unchanged.

## Verification

Command:

```bash
python work/R25-T055/check.py
```

Result:

```text
3 passed in 0.04s
```

## Mutation check

A temporary copy of the source was created with the `+` mapping deliberately changed from `operator.add` to `operator.sub`.

Command used:

```bash
python -m pytest work/R25-T055/test_voice_calculator.py -q
```

Result:

```text
1 failed, 2 passed in 0.07s
```

The failing test expected `4 + 5` to equal `9`, but the mutated implementation returned `-1`. This confirms that the tests detect the incorrect operator mapping.

The original test file was restored, and the normal verification runner was executed again successfully.

## Environment

- Python: 3.12.16
- pytest: 9.2.0

## Deliverables

- `check.py` — repeatable test runner
- `test_voice_calculator.py` — focused regression tests
- `RESULTS.md` — verification evidence