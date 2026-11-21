# R25-T034 — new_pattern.py Invariant & Property Table

Target: `new_pattern.py` — `main()` and `pattern()`

---

## 1. Source Contract & Line Citations

| Line | Code | Contract / Precondition |
|:---|:---|:---|
| Line 4 | `lines = int(input("Enter number of lines: "))` | Input must be convertible to integer via `int()`. |
| Line 5 | `if lines < 0: raise ValueError(...)` | Domain restriction: `lines >= 0`. Negative integers raise `ValueError`. |
| Line 7 | `result = pattern(lines)` | Dispatches to `pattern(lines)` to generate string. |
| Line 8 | `print(result)` | Outputs the multiline string plus trailing newline to `stdout`. |
| Line 10-15 | `except ValueError / Exception` | Handles invalid inputs and unexpected errors gracefully by printing formatted error message. |
| Line 43 | `if lines == 0: return ""` | Zero boundary: returns empty string, `main()` prints single blank line `"\n"`. |
| Line 47-50 | Loop `for i in range(lines, 0, -1)` | Generates `lines` formatted lines with `@` and `$` patterns separated by 4 spaces. |

---

## 2. Invariant Specifications

For any valid non-negative integer $n \in \mathbb{N}_0$:

### Invariant 1: Total Symbol Conservation & Symmetry
- Number of `@` characters:
  $$\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}$$
- Number of `$` characters:
  $$\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}$$
- Symmetry:
  $$\text{count}(\text{'@'}) = \text{count}(\text{'\$'}) = \frac{n(n + 1)}{2}$$

### Invariant 2: Per-Line Structural Invariant
For each line $k$ ($0 \le k < n$, 0-indexed):
- Prefix: exactly $(n - k)$ `'@'` characters.
- Separator: exactly 4 spaces (`"    "`).
- Suffix: exactly $(k + 1)$ `'$'` characters.
- Non-space characters per line: $(n - k) + (k + 1) = n + 1$.
- Total line length: $(n - k) + 4 + (k + 1) = n + 5$.

### Invariant 3: Output Line Count
- When $n = 0$: `pattern(0)` returns `""`, `main()` outputs `"\n"` (1 blank line).
- When $n > 0$: `pattern(n)` has $n$ lines separated by `\n`. With `print()`, `main()` outputs $n$ lines followed by a terminating newline.

### Invariant 4: Determinism / Idempotence
- Given the same input $n$, calling `main()` multiple times with fresh equivalent inputs produces byte-for-byte identical output.

---

## 3. Test Partition & Anchors

| Category | Input `lines` | Expected Output Description | Source Anchor / Citation |
|:---|:---|:---|:---|
| **Anchor 1** | `3` | 3 lines: `@@@    $\n@@    $$\n@    $$$` | Task anchor: `print(pattern(3))` |
| **Anchor 2** | `1` | 1 line: `@    $` | Task anchor: `print(pattern(1))` |
| **Anchor 3** | `0` | Empty pattern / blank line: `\n` | Task anchor: `print(pattern(0))` |
| **Neighbor (Derived)** | `2` | 2 lines: `@@    $\n@    $$` | Independently calculated neighbor |
| **Neighbor 2** | `4` | 4 lines: `@@@@    $\n@@@    $$\n@@    $$$\n@    $$$$` | Extended neighbor check |
| **Property Domain** | 100 cases ($0 \le n \le 50$) | Evaluated against independent oracle and property invariants | Deterministic seed `42` |
| **Invalid Domain** | Negative (`-1`, `-5`) | Prints error message: `Error: Number of lines must be non-negative` | Lines 5-6, 14-15 |
| **Invalid Domain** | Non-integer (`"abc"`, `"3.5"`) | Prints error message: `Error: Please enter a valid integer number...` | Lines 4, 11-12 |

---

## 4. Smallest Failing Example Under Mutation

| Mutation Tested | Smallest Failing Case | Expected | Mutated Output | Violated Invariant |
|:---|:---:|:---|:---|:---|
| Spacing changed from 4 to 3 spaces | $n = 1$ | `@    $\n` | `@   $\n` | Per-line length ($7 \ne 6$), separator invariant |
| Symbol changed (`@` to `#`) | $n = 1$ | `@    $\n` | `#    $\n` | Total `@` count ($1 \ne 0$), symbol symmetry |
| Off-by-one in `$` count | $n = 1$ | `@    $\n` | `@    \n` | Total `$` count ($1 \ne 0$), per-line structure |
