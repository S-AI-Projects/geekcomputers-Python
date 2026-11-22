# R25-T036 — gcd.py Refactoring & Precondition Table

Target: `gcd.py` — `gcd`

---

## 1. Source Preconditions & Citations

| Line | Original Code | Precondition & Contract |
|:---|:---|:---|
| Line 6 | `a = int(input("Enter number 1 (a): "))` | Input `a`: integer convertible. |
| Line 7 | `b = int(input("Enter number 2 (b): "))` | Input `b`: integer convertible. |
| Line 9 | `i = 1` | Loop counter initialized at positive unit divisor 1. |
| Line 10 | `gcd = -1` | Default sentinel value if loop does not run. |
| Line 11 | `while i <= a and i <= b:` | Search bounds: iterates while candidate $i \le \min(a, b)$. |
| Line 12 | `if a % i == 0 and b % i == 0:` | Divisibility test: verifies if $i$ is a common factor of both $a$ and $b$. |
| Line 13 | `gcd = i` | Updates current greatest common divisor. |
| Line 14 | `i = i + 1` | Increments candidate divisor. |
| Line 16 | `print("\nGCD of {0} and {1} = {2}".format(a, b, gcd))` | Formats and emits result to stdout. |

---

## 2. Refactoring Analysis

### What was refactored:
1. **Extracted Helper**: Extracted the compound divisibility condition `(a % i == 0 and b % i == 0)` into an explicit, intention-revealing helper function:
   ```python
   def is_common_divisor(i: int, a: int, b: int) -> bool:
       """Return True if i is a common divisor of both a and b."""
       return a % i == 0 and b % i == 0
   ```
2. **Encapsulated Function**: Encapsulated the core algorithm in `def gcd(a: int, b: int) -> int:` so it can be called programmatically.
3. **CLI Preservation**: Guarded interactive prompts under `if __name__ == "__main__":` to preserve CLI usage while allowing clean imports.

### Readability Improvement:
- Isolates the mathematical concept of "common divisibility" from the linear search traversal.
- Makes the loop body self-documenting:
  ```python
  while i <= a and i <= b:
      if is_common_divisor(i, a, b):
          result = i
      i += 1
  ```
- Retains identical algorithm, time complexity $\mathcal{O}(\min(a, b))$, ordering, return type (`int`), and side effects.

---

## 3. Fixture Matrix & Expected Outputs

| Input Pair `(a, b)` | Precondition Line Citations | Expected Result | Description / Mathematical Justification |
|:---|:---|:---:|:---|
| `(54, 24)` | Lines 9-14 | `6` | Nonzero pair: $\gcd(54, 24) = 6$ |
| `(17, 13)` | Lines 9-14 | `1` | Coprime pair: $\gcd(17, 13) = 1$ |
| `(9, 9)` | Lines 9-14 | `9` | Equal pair: $\gcd(9, 9) = 9$ |
| `(0, 5)` | Lines 10, 11 | `-1` | Zero argument: $1 \le 0$ is False, loop exits, sentinel `-1` returned |
| `(5, 0)` | Lines 10, 11 | `-1` | Zero argument: $1 \le 0$ is False, loop exits, sentinel `-1` returned |
| `(0, 0)` | Lines 10, 11 | `-1` | Both zero: loop exits, sentinel `-1` returned |
