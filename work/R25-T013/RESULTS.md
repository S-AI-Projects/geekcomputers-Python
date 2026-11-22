# Verification Evidence — R25-T013

## Target
- **Script:** ex20.py
- **Function:** `print_all`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m unittest /Users/nevilmaru009/.gemini/antigravity/scratch/geekcomputers-Python/work/R25-T013/test_ex20.py -v`

## Precondition Citations
- Line 6: `def print_all(f):` establishes file/stream input interface.
- Line 7: `print(f.read())` reads stream to EOF and emits to stdout.
- Line 10: `f.seek(0)` establishes stream pointer and mutation awareness.

## Oracle Specification
- **Independent Method:** Uses `readline()` chunked collection instead of `.read()`, appending `\n` to match standard `print()` semantics.
- **Independence:** The reference oracle runs independently without invoking the target function under test.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input | L6, L7 | `io.StringIO("")` | `stdout == "\n"`, `tell() == 0` | Matches expected | PASS |
| Ordinary input | L6, L7 | `io.StringIO("First\nSecond\n")` | `"First\nSecond\n\n"`, `tell() == 13` | Matches expected | PASS |
| Stream mutation check | L6, L7, L10 | Pointer at 0 | Advances pointer to EOF | Pointer advanced to EOF | PASS |
| 21-Input Oracle Comparison | L6, L7 | 21 diverse inputs | Exact oracle match across all 21 cases | 21/21 passed | PASS |

## Test Runner Output
```
test_all_21_inputs_against_independent_oracle (work.R25-T013.test_ex20.TestEx20PrintAllReference.test_all_21_inputs_against_independent_oracle)
Compare print_all output against independent reference oracle across 21 test inputs. ... ok
test_ordinary_input (work.R25-T013.test_ex20.TestEx20PrintAllReference.test_ordinary_input)
Ordinary input: multi-line file content. ... ok
test_smallest_valid_input (work.R25-T013.test_ex20.TestEx20PrintAllReference.test_smallest_valid_input)
Smallest valid input: empty file stream. ... ok
test_stream_mutation_advances_to_eof (work.R25-T013.test_ex20.TestEx20PrintAllReference.test_stream_mutation_advances_to_eof)
Test stream position mutation: print_all moves file pointer from 0 to EOF. ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

**Exit Code:** 0
