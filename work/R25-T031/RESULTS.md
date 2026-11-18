# Test Results & Evidence — R25-T031

## Environment & Tool Versions
- **Date:** 2026-11-18
- **Task:** R25-T031
- **Target:** `recursive-fibonacci.py` (`fib` function)
- **Python:** 3.12.16
- **Pytest:** 9.2.0
- **Git:** 2.55.0

## Execution Command
```bash
python3 work/R25-T031/check.py
```

## Native Check Command
```bash
pytest -v work/R25-T031/test_recursive_fibonacci.py
```

## Summary
- **Total Tests Collected:** 14
- **Passed:** 14
- **Failed:** 0
- **Duration:** 0.08s
- **Exit Code:** 0

## Stated Fixture Results (Zero-Based Indexing)
| Index (`n`) | Test Category | Expected Value | Actual Value | Result |
| :---: | :--- | :---: | :---: | :---: |
| `0` | Smallest supported input (base case root) | `0` | `0` | PASS |
| `1` | Base case boundary | `1` | `1` | PASS |
| `2` | Repeated-value boundary (`fib(2) == fib(1)`) | `1` | `1` | PASS |
| `5` | Ordinary input | `5` | `5` | PASS |
| `10` | Larger ordinary input | `55` | `55` | PASS |

## Invariant & Contract Regression Checks
- **No Observable Mutation:** Caller arguments and module globals remain strictly unmutated.
- **Idempotency:** Repeated executions across all fixture indices return identical results.
- **External I/O Isolation:** Verified zero calls to `print`, `open`, or network sockets.
- **Contract & Signature:** Signature `fib(n)` documented with clear docstring, returns integer.

