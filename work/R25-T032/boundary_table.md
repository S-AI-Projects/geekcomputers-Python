# R25-T032 — simpleInterest Boundary Table

Source: `simpleInterest.py`

## Source Preconditions & Citations
- **Source Line 1:** `principle = float(input("Enter the principle amount:"))`
  - Precondition: `principle` must be a numeric value convertible to `float`.
- **Source Line 2:** `time = int(input("Enter the time(years):"))`
  - Precondition: `time` must be an integer (or numeric value representing whole years).
- **Source Line 3:** `rate = float(input("Enter the rate:"))`
  - Precondition: `rate` must be a numeric value convertible to `float`.
- **Source Line 4:** `simple_interest = (principle * time * rate) / 100`
  - Precondition: Arithmetic multiplication and division by 100.
- **Source Line 5:** `print("The simple interest is:", simple_interest)`
  - Output display format.

---

## Input Partition Table

| Category | Input (`principle`, `time`, `rate`) | Expected Result | Source Contract / Line Citation | Test Function |
| :--- | :--- | :---: | :--- | :--- |
| **Valid Interior (Ordinary Input)** | `principle=1000.0, time=2, rate=5.0` | `100.0` | Line 1 (`float`), Line 2 (`int`), Line 3 (`float`), Line 4 (formula) | `test_simple_interest_ordinary_input` |
| **Valid Boundary (Smallest Valid Input - Zero Boundary)** | `principle=0.0, time=0, rate=0.0` | `0.0` | Line 1 (`0.0`), Line 2 (`0`), Line 3 (`0.0`), Line 4 (formula) | `test_simple_interest_smallest_valid_input_zero` |
| **Valid Boundary (Smallest Positive Non-Zero Input)** | `principle=1.0, time=1, rate=1.0` | `0.01` | Line 1 (`1.0`), Line 2 (`1`), Line 3 (`1.0`), Line 4 `(1*1*1)/100 = 0.01` | `test_simple_interest_smallest_positive_input` |
| **Boundary (Zero Principle)** | `principle=0.0, time=2, rate=5.0` | `0.0` | Line 1 (`0.0`), Line 4 (`0.0 * 2 * 5.0 / 100 = 0.0`) | `test_simple_interest_zero_principle_boundary` |
| **Boundary (Zero Time)** | `principle=1000.0, time=0, rate=5.0` | `0.0` | Line 2 (`0`), Line 4 (`1000.0 * 0 * 5.0 / 100 = 0.0`) | `test_simple_interest_zero_time_boundary` |
| **Boundary (Zero Rate)** | `principle=1000.0, time=2, rate=0.0` | `0.0` | Line 3 (`0.0`), Line 4 (`1000.0 * 2 * 0.0 / 100 = 0.0`) | `test_simple_interest_zero_rate_boundary` |
| **Explicitly Unsupported (Incompatible Types)** | `principle=None, time=2, rate=5.0` | `TypeError` | Python standard multiplication fails on `NoneType` | `test_simple_interest_unsupported_non_numeric_type` |

---

## Public Behavior & Design Notes
1. **Inputs:** `principle` (float/numeric), `time` (int/numeric), `rate` (float/numeric).
2. **Return:** `float` interest amount.
3. **Mutation:** None. Pure mathematical calculation.
4. **Policy on Unspecified Behavior:** As specified in task requirements ("Do not add rejection rules for behavior the source leaves undefined. No arbitrary TypeError/RangeError policy is imposed across unrelated functions"), no arbitrary guards are added for negative inputs; standard mathematical evaluation is preserved.

