# Verification Evidence — R25-T015

## Target
- **Script:** diamond.py
- **Function:** `draw_diamond`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m unittest /Users/nevilmaru009/.gemini/antigravity/scratch/geekcomputers-Python/work/R25-T015/test_diamond.py -v`

## Precondition Citations
- Line 1: `def draw_diamond(n):` input interface with dependency seam `output_fn=print`.
- Line 2: `if n % 2 != 0:` parity check (odd number requirement).
- Lines 4-5: Upper pyramid expansion step by 2.
- Lines 9-10: Lower inverted pyramid contraction step by 2.
- Line 14: Non-odd input rejection fallback.

## Determinism & Seam Architecture
- **Dependency Seam:** Added optional `output_fn=print` parameter defaulting to built-in `print`.
- **Caller Compatibility:** Current 1-argument calls `draw_diamond(n)` behave 100% identically.
- **Repeatability Proof:** Tested `draw_diamond(3)` before and after an intervening `draw_diamond(7)` call; proved zero state pollution across invocations.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (n=1) | L2, L4-5 | `n=1` | `["*"]` | `["*"]` | PASS |
| Ordinary input (n=3) | L2, L4-5, L9-10 | `n=3` | `[" * ", "***", " * "]` | `[" * ", "***", " * "]` | PASS |
| Ordinary input (n=5) | L2, L4-5, L9-10 | `n=5` | 5-line diamond | 5-line diamond | PASS |
| Even number rejection (n=4) | L2, L14 | `n=4` | `["Not an odd number..."]` | `["Not an odd number..."]` | PASS |
| Repeatability & Isolation | L1, L2, L4, L9 | `n=3` twice with intervening `n=7` | Identical output across fresh & subsequent runs | Exact match | PASS |

## Test Runner Output
```
test_even_number_rejection (work.R25-T015.test_diamond.TestDiamondDeterministicExecution.test_even_number_rejection)
Even input rejection: n=4. ... ok
test_ordinary_input_five (work.R25-T015.test_diamond.TestDiamondDeterministicExecution.test_ordinary_input_five)
Ordinary input: n=5. ... ok
test_ordinary_input_three (work.R25-T015.test_diamond.TestDiamondDeterministicExecution.test_ordinary_input_three)
Ordinary input: n=3. ... ok
test_repeatability_and_input_isolation (work.R25-T015.test_diamond.TestDiamondDeterministicExecution.test_repeatability_and_input_isolation)
Assert that running a fixture twice with an intervening distinct call produces identical output. ... ok
test_smallest_valid_input_one (work.R25-T015.test_diamond.TestDiamondDeterministicExecution.test_smallest_valid_input_one)
Smallest valid input: n=1. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

**Exit Code:** 0
