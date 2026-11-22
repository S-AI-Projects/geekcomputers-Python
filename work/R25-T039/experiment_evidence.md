# R25-T039: Complexity and Correctness Experiment Evidence

**Target Item:** `Sum of digits of a number.py`  
**Target Function:** `get_integer` (and `addition`)

## 1. Environment & Tool Versions

- **OS:** macOS (darwin)
- **Python:** 3.12.16
- **pytest:** 9.2.0
- **Runner Command:** `python3 work/R25-T039/check.py`

## 2. Pre-change Analysis of `get_integer`

- **Public Inputs:** None (calls standard library `input()`).
- **Result:** Returns `int(num)` if a valid numeric string is entered within 3 attempts; implicitly returns `None` after 3 failed attempts.
- **Mutation Behavior:** Pure; does not mutate any caller-owned or global state.
- **External Dependencies:** `builtins.input`, `builtins.print`, `builtins.int`, `str.isnumeric`.

## 3. Complexity Formulation

- **Input-Size Variable:**
  - Let $d$ be the number of characters (digits) in the input string (or $d = \lfloor \log_{10}(|num|) \rfloor + 1$ for integer $num$).
- **Worst-Case Theoretical Complexity:**
  - `num.isnumeric()` scans all $d$ characters $\to O(d)$ time.
  - `int(num)` parses a base-10 digit string $\to O(d)$ to $O(d \log d)$ time in Python arbitrary precision.
  - Number of retry attempts is bounded by a constant (3).
  - Total worst-case time complexity: $O(d)$.
  - Total space complexity: $O(d)$ to store string and integer representation.
- **Empirical Observations:**
  - Isolating algorithm operations from startup, I/O, and compilation shows median runtimes scaling cleanly across $d \in \{100, 1000, 3000\}$:
    - $d = 100$: Median $0.62\ \mu\text{s}$
    - $d = 1000$: Median $4.38\ \mu\text{s}$
    - $d = 3000$: Median $33.92\ \mu\text{s}$
  - All measured outputs verified 100% correct outside the timed intervals.

## 4. Source Anchors and Independently Calculated Derived Inputs

| Identifier | Type | Input | Expected Output | Independent Calculation / Source |
|------------|------|-------|-----------------|----------------------------------|
| `addition(123)` | Source Anchor 1 | `123` | `6` | $1 + 2 + 3 = 6$ (docstring line 44) |
| `addition(-784)` | Source Anchor 2 | `-784` | `19` | $|-784| = 784 \implies 7 + 8 + 4 = 19$ (docstring line 46) |
| `addition(124)` | Derived Neighbor 1 | `124` | `7` | $1 + 2 + 4 = 7$ (anchor $123 + 1$) |
| `addition(-785)` | Derived Neighbor 2 | `-785` | `20` | $|-785| = 785 \implies 7 + 8 + 5 = 20$ (anchor $-784 - 1$) |
| `addition(0)` | Boundary | `0` | `0` | Sum of digits of 0 is 0 |

## 5. Timing Summary Table

| Input Size ($d$ digits) | Repetitions | Min ($\mu$s) | Median ($\mu$s) | Max ($\mu$s) | Range ($\mu$s) | Correctness |
|------------------------|-------------|--------------|-----------------|--------------|----------------|-------------|
| 100 | 5 | 0.38 | 0.62 | 0.92 | 0.54 | 5/5 (100%) |
| 1000 | 5 | 4.33 | 4.38 | 6.00 | 1.67 | 5/5 (100%) |
| 3000 | 5 | 31.04 | 33.92 | 36.17 | 5.12 | 5/5 (100%) |
