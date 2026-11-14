# R25-T051 — Exception Handling in Python

## Environment
- Python: 3.12.16
- Pytest: 9.2.0
- Platform: macOS
- Git branch: student/e26b07f0863

## Source inspection
File: Exception_Handling_in_Python.py

- Line 70: l = [1, 2, 3, 4] — source fixture.
- Line 73: print(l[4]) — out-of-range access.
- Line 75: catches IndexError.
- Line 76: prints the out-of-range message.

The source is a standalone script. It has no function return value and does not mutate the list.

## Independent expected results

| Input | Expected |
|---|---|
| [1, 2, 3, 4], index 0 | 1 |
| [1, 2, 3, 4], index 2 | 3 |
| [1, 2, 3, 4], index 3 | 4 |
| [1, 2, 3, 4], index 4 | IndexError |
| [1, 1, 2, 2], index 1 | 1 |

Expected mutation: none.

## Baseline execution

Command:
(cd work/R25-T051/baseline-run && python ../../../Exception_Handling_in_Python.py > ../baseline_output.txt 2>&1; echo "Exit code: $?")

Actual exit code: 1.

The script printed its exception-handling messages and then raised the intentional
Exception("You are legally underage!!!") at source line 118.

The script also created aaa.txt in the baseline working directory.

Baseline output: baseline_output.txt
Baseline copy: baseline_expected.txt

## Regression tests

Command:
python -m pytest -v work/R25-T051/test_exception_handling.py

Actual result: 7 passed, 0 failed.

## Focused runner

Command:
python work/R25-T051/check.py

Actual result: 7 passed, 0 failed.

The focused runner propagates pytest's exit code.

## Test coverage

1. Smallest valid index — expected 1.
2. Ordinary index — expected 3.
3. Last valid index — expected 4.
4. Out-of-range index — expected IndexError.
5. Repeated-value input — expected 1.
6. List remains unchanged after indexing.
7. Original script prints the expected exception-handling messages,
   closes the mocked file, and raises its expected final custom exception.

## Implementation changes

Exception_Handling_in_Python.py was not modified.
No helper functions or main guard were added because the task owner
did not permit restructuring the original source.
