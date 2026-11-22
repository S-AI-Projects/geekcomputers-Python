# Verification Evidence — R25-T009

## Target
- **Script:** recyclebin.py
- **Function:** `sid2user`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest /Users/krishna/SnAIproject/work/R25-T009/test_recyclebin.py -v --tb=short`

## Precondition Citations
- Line 20: `sid2user(sid)` function signature
- Line 21: `OpenKey(HKEY_LOCAL_MACHINE, ...)` registry key lookup
- Line 25: `QueryValueEx(key, 'ProfileImagePath')` value extraction
- Line 26: `user = value.split('\')[-1]` path parsing
- Line 28: `except Exception: return sid` fallback behavior
- Line 32: `dirs = ["c:\\Recycler\\", "C:\\Recycled\\", "C:\\$RECYCLE.BIN\\"]`

## Complexity Analysis & Work Scaling
- **Input size variable ($n$):** Length of the `ProfileImagePath` string.
- **Theoretical Worst-Case Complexity:** $O(n)$ time to scan and split the string on backslash delimiters; $O(n)$ space to store split segments.
- **Measured Operations:** Exactly 1 `OpenKey` and 1 `QueryValueEx` call per resolution.
- **Timing Independence:** All assertions evaluate functional correctness and call counts; zero assertions rely on wall-clock speed.

## Verification Matrix
| Scenario | Preconditions | Literal Input | Expected Output | Actual Result | Status |
|---|---|---|---|---|---|
| Smallest valid input | L20, L25, L26 | `'S-1-0-0'` | `'Nobody'` | `'Nobody'` | PASS |
| Ordinary valid input | L20, L25, L26 | Admin SID | `'Administrator'` | `'Administrator'` | PASS |
| Fallback on missing key | L28 | `'S-1-5-UNKNOWN'` | `'S-1-5-UNKNOWN'` | `'S-1-5-UNKNOWN'` | PASS |
| Algorithmic scaling ($n=20..20000$) | L26 | Scaling path depths | Exact usernames across all scales | All depths parsed correctly | PASS |

## Test Runner Output
```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.14/bin/python3
cachedir: .pytest_cache
rootdir: /Users/krishna/SnAIproject
collecting ... collected 4 items

work/R25-T009/test_recyclebin.py::TestSid2UserWorkAndScaling::test_smallest_valid_input_nobody PASSED [ 25%]
work/R25-T009/test_recyclebin.py::TestSid2UserWorkAndScaling::test_ordinary_input_admin PASSED [ 50%]
work/R25-T009/test_recyclebin.py::TestSid2UserWorkAndScaling::test_unregistered_sid_fallback PASSED [ 75%]
work/R25-T009/test_recyclebin.py::TestSid2UserWorkAndScaling::test_algorithmic_work_scaling PASSED [100%]

============================== 4 passed in 0.02s ===============================
```

**Exit Code:** 0
