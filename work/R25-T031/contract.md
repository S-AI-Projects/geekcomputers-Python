# Contract Evidence — Recursive Fibonacci

## Target
- **Source File:** `recursive-fibonacci.py`
- **Function:** `fib(n)` (line 1)

## Public Interface & Preconditions
- **Inputs:** `n` (int) — Non-negative integer index in the Fibonacci sequence ($n \ge 0$).
- **Return Value:** `int` — The $n$-th Fibonacci number using standard zero-based indexing:
  - $F(0) = 0$
  - $F(1) = 1$
  - $F(n) = F(n-1) + F(n-2)$ for $n \ge 2$
- **Preconditions:**
  - `n` must be an integer $\ge 0$.
  - Indexing is zero-based as established by base cases `fib(0) == 0` and `fib(1) == 1`.

## Stated Fixture & Expected vs Actual Results
| Index (`n`) | Role / Category | Independent Expected Output | Actual Output | Status |
| :---: | :--- | :---: | :---: | :---: |
| `0` | Smallest supported input (base case root) | `0` | `0` | Passed |
| `1` | Base case boundary | `1` | `1` | Passed |
| `2` | Repeated value boundary (first recursive step) | `1` | `1` | Passed |
| `5` | Ordinary input | `5` | `5` | Passed |
| `10` | Larger ordinary input | `55` | `55` | Passed |

## Domain Boundaries & Test Categories
1. **Smallest Supported Input (`n = 0`):**
   - Evaluates the lower boundary of valid non-negative integer domain.
   - Expected: `0`.
2. **Repeated-Value Domain Boundary (`n = 1` and `n = 2`):**
   - `fib(1) == 1` and `fib(2) == 1`.
   - Distinct inputs producing the same output value; marks transition from base case to recursive branching.
3. **Ordinary Inputs (`n = 5`, `n = 10`):**
   - Verifies recursive accumulation and correctness across multiple levels of recursion.
   - Expected: `fib(5) == 5`, `fib(10) == 55`.

## Observable Mutation Analysis
- `fib(n)` takes an integer parameter `n` which is immutable in Python.
- No module-level global variables are declared or modified.
- No attributes on caller objects or external data structures are modified.
- Function execution is idempotent and pure.

## External Dependencies & I/O
- No external packages required; uses standard Python built-ins.
- No network access, disk file I/O, system clock access, or GUI operations.
- All external I/O is mocked/verified absent during testing.

## Baseline Findings
- Before contract lockdown, the source `recursive-fibonacci.py` had no docstring or explicit contract beside `fib`.
- The baseline implementation conforms to the expected 0-based mathematical Fibonacci sequence for all non-negative integers in the fixture ($0, 1, 2, 5, 10$).
- Added docstring contract beside `fib` and created focused regression test suite in `work/R25-T031/`.

