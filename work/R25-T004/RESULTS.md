# Verification Evidence — R25-T004

## Target
- **Script:** how to display the fibonacci sequence up to n-.py
- **Function:** `fibonacci_sequence` / `how_to_display_the_fibonacci_sequence_up_to_n`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest /Users/krishna/SnAIproject/work/R25-T004/test_fibonacci.py -v --tb=short`

## Precondition Citations
- Line 6: `n1, n2 = 0, 1` establishing F(0)=0 and F(1)=1
- Line 10: `nterms <= 0` input validity guard
- Line 17: `nth = n1 + n2` defining recurrence F(n+2) = F(n+1) + F(n)

## Fixture and Invariant Results
| Check Scenario | Precondition | Input / Index | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Fixture Index 0 | L6 | Index 0 | `0` | `0` | PASS |
| Fixture Index 1 | L6 | Index 1 | `1` | `1` | PASS |
| Fixture Index 2 | L6, L17 | Index 2 | `1` | `1` | PASS |
| Fixture Index 5 | L17 | Index 5 | `5` | `5` | PASS |
| Fixture Index 10 | L17 | Index 10 | `55` | `55` | PASS |
| Invariant F(n+2)=F(n+1)+F(n) | L17 | Indices 0..22 | Exact equality across range | Exact equality across range | PASS |
| Smallest valid input | L10 | `nterms=1` | `[0]` | `[0]` | PASS |
| Deliberate mutant detection | L17 | `nth = n1 + n2 + 1` | Invariant failure | Detected invariant failure | PASS |

## Test Runner Output
```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.14/bin/python3
cachedir: .pytest_cache
rootdir: /Users/krishna/SnAIproject
collecting ... collected 4 items

work/R25-T004/test_fibonacci.py::TestFibonacciInvariant::test_fixture_values_at_specified_indices PASSED [ 25%]
work/R25-T004/test_fibonacci.py::TestFibonacciInvariant::test_recurrence_invariant_across_range PASSED [ 50%]
work/R25-T004/test_fibonacci.py::TestFibonacciInvariant::test_smallest_valid_input_boundaries PASSED [ 75%]
work/R25-T004/test_fibonacci.py::TestFibonacciInvariant::test_deliberate_mutant_fails_invariant PASSED [100%]

============================== 4 passed in 0.02s ===============================
```

**Exit Code:** 0
