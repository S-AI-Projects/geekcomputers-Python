# Verification Evidence — R25-T024 (power_of_two.py)

## Environment & Tool Versions
- **Python Version:** 3.13.14
- **Platform:** macOS-27.3-arm64-arm-64bit-Mach-O
- **Runner:** /Users/namanlunia/SandAI/.venv/bin/python3
- **Target File:** power_of_two.py
- **Test Suite:** work/R25-T024/test_power_of_two.py

## Executed Command
```bash
/Users/namanlunia/SandAI/.venv/bin/python3 -m pytest -v /Users/namanlunia/SandAI/geekcomputers-Python/work/R25-T024/test_power_of_two.py
```

## Precondition Source Lines Cited
- `power_of_two.py#L22`: `a = int(input("Enter a number"))` (stdin integer conversion)
- `power_of_two.py#L23`: `if a & (a - 1) == 0:` (bitwise invariant check)
- `power_of_two.py#L24`: `print("It comes in  power series of 2")` (power of 2 output)
- `power_of_two.py#L26`: `print("It does not come in  power series of 2")` (non-power output)

## Invariant Definition & Property Verification
The mathematical invariant for any integer $n \ge 1$ is:
`n is a power of 2 <==> bin(n).count('1') == 1 <==> (n & (n - 1) == 0)`.
A deterministic pseudo-random generator (seed=42) produced 100 bounded cases (50 powers of two and 50 non-powers of two up to $2^{30}$). Every case satisfied the property.

| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest input | L22-24 | `1` ($2^0$) | 'It comes in  power series of 2' | 'It comes in  power series of 2' | PASS |
| Ordinary power of 2 | L22-24 | `8` ($2^3$) | 'It comes in  power series of 2' | 'It comes in  power series of 2' | PASS |
| Ordinary non-power | L22, L26 | `6` | 'It does not come in  power series of 2' | 'It does not come in  power series of 2' | PASS |
| 100 Bounded Cases | L22-26 | 100 random values (seed=42) | Matches `bin(n).count('1') == 1` | 100/100 matched | PASS |
| Mutant Sensitivity | Inverted invariant | `1` | Mutant fails assertion | Mutant caught | PASS |

## Pytest Console Output
```
============================= test session starts ==============================
platform darwin -- Python 3.13.14, pytest-9.2.0, pluggy-1.7.0 -- /Users/namanlunia/SandAI/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/namanlunia/SandAI/geekcomputers-Python
collecting ... collected 4 items

work/R25-T024/test_power_of_two.py::TestPowerOfTwoInvariant::test_smallest_valid_input PASSED [ 25%]
work/R25-T024/test_power_of_two.py::TestPowerOfTwoInvariant::test_ordinary_inputs PASSED [ 50%]
work/R25-T024/test_power_of_two.py::TestPowerOfTwoInvariant::test_invariant_property_100_bounded_valid_cases PASSED [ 75%]
work/R25-T024/test_power_of_two.py::TestPowerOfTwoInvariant::test_mutant_sensitivity_smallest_failing_example PASSED [100%]

============================== 4 passed in 0.04s ===============================

```

**Exit Code:** 0
