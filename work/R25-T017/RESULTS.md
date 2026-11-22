# Verification Evidence — R25-T017

## Target
- **Script:** rangoli.py
- **Function:** `print_rangoli`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m unittest /Users/nevilmaru009/.gemini/antigravity/scratch/geekcomputers-Python/work/R25-T017/test_rangoli.py -v`

## Precondition Citations
- Line 5: `def print_rangoli(n):` input size parameter.
- Line 7: `width = 4 * n - 3` determines line width and centering canvas.
- Line 14: `chr(96 + n - j)` descending alphabet loop.
- Line 19: `chr(97 + n - k)` ascending alphabet loop.
- Lines 24, 38: `string.center(width, "-")` centered line rendering.

## Decisive State Transition
- Trailing hyphen suppression occurs on line 15 & 21 when `len(string) == width` at the center row (`i = n`).
- In non-center rows (`i < n`), uncentered strings carry a trailing hyphen (e.g. `'c-'` of length 2), which Python's `center(9, '-')` cleanly absorbs by padding 4 dashes on the left and 3 on the right (`'----c----'`).

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (n=1) | L7, L14 | `n=1` | `"a\n"` | `"a\n"` | PASS |
| Ordinary input (n=3) doc example | L7, L14, L19, L24 | `n=3` | 5-line diamond rangoli | 5-line diamond rangoli | PASS |
| Decisive state transition | L7, L15, L21, L24 | `n=3, width=9` | Exact center boundary & centering mechanics | Exact match | PASS |

## Test Runner Output
```
test_decisive_state_transition_center_boundary (work.R25-T017.test_rangoli.TestRangoliExecutableDocumentation.test_decisive_state_transition_center_boundary)
Test the state transition where len(string) reaches width and suppresses trailing hyphen. ... ok
test_ordinary_input_three_documentation_example (work.R25-T017.test_rangoli.TestRangoliExecutableDocumentation.test_ordinary_input_three_documentation_example)
Ordinary input: n=3 matching the docstring worked example. ... ok
test_smallest_valid_input_one (work.R25-T017.test_rangoli.TestRangoliExecutableDocumentation.test_smallest_valid_input_one)
Smallest valid input: n=1. ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

**Exit Code:** 0
