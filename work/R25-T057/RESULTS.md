# R25-T057 — Runnable Random Password Generator Example

## Objective

Publish an executable worked example for `Random Password Generator.py`,
showing the character pool, selected characters, and final password.

## Original source inspection

File: `Random Password Generator.py`

- Lines 3–6: Define lowercase letters, uppercase letters, digits, and symbols.
- Line 8: Combine the four groups into the character pool.
- Line 9: Set the password length to 8.
- Line 10: Select distinct characters using `random.sample()` and join them.
- Line 11: Print the generated password.

The original source file was not modified.

## Inputs and expected results

The source fixes the password length at 8, so the smallest supported
execution uses eight selected characters.

| Case | Selected characters | Expected password |
|---|---|---|
| Smallest supported execution | `abcdefgh` | `abcdefgh` |
| Ordinary execution | `aB3!cD4@` | `aB3!cD4@` |

The tests mock `random.sample()` to make the selections deterministic.

## Intermediate state

For the ordinary example:

1. Lowercase letters: 26 characters.
2. Uppercase letters: 26 characters.
3. Digits: 10 characters.
4. Symbols: 8 characters.
5. Combined pool: 70 characters.
6. Requested selection length: 8.
7. Selected characters: `['a', 'B', '3', '!', 'c', 'D', '4', '@']`.
8. Joining the selected characters produces `aB3!cD4@`.

The decisive state transition is joining the selected character list
into the final password.

## Worked example output

Command:

    python3 work/R25-T057/example.py

Expected and actual output:

    Character pool size: 70
    Requested length: 8
    Selected characters: ['a', 'B', '3', '!', 'c', 'D', '4', '@']
    Final password: aB3!cD4@

The automated test executes the example and asserts its exact standard output.

## Test isolation

The original generator is loaded in the focused tests with `random.sample`
mocked. The example uses a fixed selection so its output is reproducible.
No external I/O is required.

## Verification

Focused test command:

    python -m pytest work/R25-T057/test_password_generator.py -q

Result:

    3 passed in 0.08s

Required runner command:

    python3 work/R25-T057/check.py

Result:

    3 passed in 0.08s

## Environment

- Python 3.12.16
- pytest 9.2.0

## Deliverables

- `example.py` — runnable deterministic worked example
- `test_password_generator.py` — focused behavior and output tests
- `check.py` — repeatable test runner
- `RESULTS.md` — inputs, intermediate state, expected output, and evidence
