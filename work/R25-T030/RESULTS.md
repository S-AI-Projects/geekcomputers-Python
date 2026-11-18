# Verification Evidence — R25-T030 (pscheck.py)

## Environment & Tool Versions
- **Python Version:** 3.13.14
- **Platform:** macOS-27.3-arm64-arm-64bit-Mach-O
- **Runner:** /Users/namanlunia/SandAI/.venv/bin/python3
- **Target File:** pscheck.py (function `ps`)
- **Test Suite:** work/R25-T030/test_pscheck.py

## Executed Command
```bash
/Users/namanlunia/SandAI/.venv/bin/python3 -m pytest -v /Users/namanlunia/SandAI/geekcomputers-Python/work/R25-T030/test_pscheck.py
```

## Preconditions & Source Lines Cited
- `pscheck.py#L41`: `program = input("Enter the name of the program to check: ")` (interactive query input)
- `pscheck.py#L45`: `output = commands.getoutput("ps -f|grep " + program)` (shell process execution)
- `pscheck.py#L46`: `proginfo = string.split(output)` (whitespace field tokenization into >= 6 tokens)
- `pscheck.py#L52`: `proginfo[5]` (Full path)
- `pscheck.py#L55`: `proginfo[0]` (Owner field)
- `pscheck.py#L58`: `proginfo[1]` (Process ID)
- `pscheck.py#L61`: `proginfo[2]` (Parent process ID)
- `pscheck.py#L64`: `proginfo[4]` (Time started)
- `pscheck.py#L66`: `except:` failure boundary for missing / malformed outputs

## Fixtures and Expected vs Actual Outputs
### 1. Smallest Valid Input
- **Input Program:** `"a"`
- **Mocked ps output:** `"u 1 0 c t /a"`
- **Expected stdout:**
```

    Full path:		 /a 
    Owner:			 u 
    Process ID:		 1 
    Parent process ID:	 0 
    Time started:		 t
```
- **Actual stdout:**
```

    Full path:		 /a 
    Owner:			 u 
    Process ID:		 1 
    Parent process ID:	 0 
    Time started:		 t
```
- **Status:** PASS (contract matches exact expected formatting)

### 2. Ordinary Valid Input
- **Input Program:** `"python"`
- **Mocked ps output:** `"root 1234 1 0 10:00 /usr/bin/python"`
- **Expected stdout:**
```

    Full path:		 /usr/bin/python 
    Owner:			 root 
    Process ID:		 1234 
    Parent process ID:	 1 
    Time started:		 10:00
```
- **Actual stdout:**
```

    Full path:		 /usr/bin/python 
    Owner:			 root 
    Process ID:		 1234 
    Parent process ID:	 1 
    Time started:		 10:00
```
- **Status:** PASS (contract matches exact expected formatting)

## Mutation Sensitivity Test Results
- **Named Assertion:** `assert_owner_field(stdout, expected_owner)`
- **Deliberate Mutant:** 1-line indexing mistake in `ps()` swapping `proginfo[0]` with `proginfo[1]` (Owner reads PID).
- **Original Code Result:** PASS
- **Mutant Code Result:** FAIL (Caught as expected)
- **Mutant Semantic Failure Message:**
```
Semantic regression detected: expected 'Owner:\t\t\t root' in stdout, got:

    Full path:		 /usr/bin/python 
    Owner:			 1234 
    Process ID:		 1234 
    Parent process ID:	 1 
    Time started:		 10:00

```

## Pytest Console Output
```
============================= test session starts ==============================
platform darwin -- Python 3.13.14, pytest-9.2.0, pluggy-1.7.0 -- /Users/namanlunia/SandAI/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/namanlunia/SandAI/geekcomputers-Python
collecting ... collected 5 items

work/R25-T030/test_pscheck.py::test_smallest_valid_input PASSED          [ 20%]
work/R25-T030/test_pscheck.py::test_ordinary_valid_input PASSED          [ 40%]
work/R25-T030/test_pscheck.py::test_mutation_detection_owner_field_swap PASSED [ 60%]
work/R25-T030/test_pscheck.py::test_failure_behavior_empty_or_malformed_output PASSED [ 80%]
work/R25-T030/test_pscheck.py::test_input_isolation_and_idempotency PASSED [100%]

============================== 5 passed in 0.03s ===============================

```

**Exit Code:** 0
