# R25-T037 — Executable Documentation & Example Table

Target: `simple_calculator.py` — `add` (line 18)

---

## 1. Source Preconditions & Citations

| Line | Original Code | Precondition & Contract |
|:---|:---|:---|
| Line 8 | `>>> add(2, 3)` | Task anchor: module-level doctest for `add`. Expected output: `5`. |
| Line 10 | `>>> subtract(10, 4)` | Task anchor: module-level doctest for `subtract`. Expected output: `6`. |
| Line 12 | `>>> multiply(3, 4)` | Task anchor: module-level doctest for `multiply`. Expected output: `12`. |
| Line 14 | `>>> divide(8, 2)` | Module-level doctest for `divide`. Expected output: `4.0`. |
| Line 18 | `def add(x: float, y: float) -> float:` | Precondition: `x` and `y` are numeric inputs supporting `+`. |
| Line 20 | `return x + y` | Contract: evaluates arithmetic sum and returns result. |
| Line 43 | `print(f"{num1} + {num2} = {add(num1, num2)}")` | CLI integration: formats and prints addition output. |

---

## 2. Decisive State Transition Analysis

The calculation in `add(x, y)` has a single, decisive state transition:

```
[State 0: Inputs Bound]
  x = 2 (float/int)
  y = 3 (float/int)
        │
        ▼
[Decisive Transition: Binary Operator Evaluation]
  x + y  -->  2 + 3  -->  5
        │
        ▼
[State 1: Return Value Produced]
  result = 5
```

- **Explanation**: The decisive transition is the binary operator evaluation `x + y`: the function transitions from holding two distinct operand states to producing their synthesized numeric sum. It returns this value immediately without retaining state or introducing side effects.

---

## 3. Fixture Matrix & Expected Outputs

| Category | Input `(x, y)` | Precondition Line Citations | Expected Result | Description |
|:---|:---|:---:|:---:|:---|
| **Anchor 1** | `(2, 3)` | Lines 8, 18, 20 | `5` | Integer addition anchor |
| **Anchor 2** | `(10, 4)` (via subtract) | Lines 10, 24 | `6` | Anchor subtraction check |
| **Anchor 3** | `(3, 4)` (via multiply) | Lines 12, 30 | `12` | Anchor multiplication check |
| **Derived Neighbor 1** | `(3, 4)` (via add) | Lines 18, 20 | `7` | Neighboring addition from anchor (3, 4) |
| **Derived Neighbor 2** | `(2.5, 3.5)` | Lines 18, 20 | `6.0` | Floating point neighbor to (2, 3) |
| **Boundary (Zero)** | `(0, 0)` | Lines 18, 20 | `0` | Additive identity boundary |
| **Negative Operand** | `(-5, 5)` | Lines 18, 20 | `0` | Additive inverse |
| **Mixed Signs** | `(10, -3)` | Lines 18, 20 | `7` | Positive + negative operand |
| **Float Precision** | `(0.1, 0.2)` | Lines 18, 20 | `0.30000000000000004` | Standard IEEE-754 floating point addition |
| **CLI Interaction** | `"1"`, `"2"`, `"3"` | Line 43 | `"2.0 + 3.0 = 5.0"` | Interactive console execution |
