## Description

This PR implements task R25-T035 for `get_likes_on_FB.py`. It establishes a dependency seam for deterministic execution, making verification repeatable and isolated without live Facebook network access or external credentials. It preserves existing public interfaces, constants, and caller contracts while adding comprehensive repeatability and input-isolation regression tests.

## Related Issue

Fixes: #37

## Type of Change

- [x] Bug Fix
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made

- **`get_likes_on_FB.py`**:
  - Introduced the `get_likes_on_FB(userId, accessToken="TOKENVALUE", limit=100, opener=None)` function seam with dependency injection for `opener`.
  - Added defaults for `accessToken`, `limit`, and `opener` so existing callers and unmocked invocations are preserved.
  - Guarded CLI argument consumption under `if __name__ == "__main__":`, allowing clean imports without `IndexError`.
  - Added Python 2 and Python 3 compatibility handling for `urllib.request.urlopen` and UTF-8 string formatting.
  - Documented contract, preconditions, and source line citations (lines 7, 8, 9, 11-18, 19, 20, 22, 24, 25-27, 29-32, 33-36, 37, 38-48).
- **`work/R25-T035/test_get_likes_on_fb.py`**:
  - Smallest valid input test: single post with minimal fields (`created_time` only), asserting exact stdout and parsed record values against independent calculations.
  - Ordinary input test: post with explicit `shares` and `likes` counts, asserting exact output calculations.
  - Repeatability tests: running the same fixture twice in fresh isolated state produces identical output.
  - Input isolation tests: executing fixture A, then an intervening fixture B, then fixture A again proves earlier runs cannot alter later results.
  - Seam and contract verification: asserts URL formatting matches contract and parameters have caller-preserving defaults.
- **`work/R25-T035/check.py`**:
  - Focused test runner executing pytest, recording outputs and tool versions, and propagating failures.
- **`work/R25-T035/baseline.txt`**:
  - Baseline analysis recording environment, observable dependencies, source line citations, and fixture specifications.
- **`work/R25-T035/dependency_table.md`**:
  - Dependency audit and precondition matrix.
- **`work/R25-T035/results.txt`**:
  - Test execution results (8 passed in 0.07s).

## Screenshots / Recordings

N/A — command-line utility.

## Testing

Tested locally using Python 3.12.16 and pytest 9.2.0:

```bash
source .venv/bin/activate
python3 work/R25-T035/check.py
```

Result:
```
============================== 8 passed in 0.07s ===============================
All R25-T035 checks PASSED.
Exit code: 0
```

## Checklist

- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes

- All tests operate completely in memory without live network access, a real user account, or GUI interaction.
- The introduced `opener` parameter defaults to `urllib.request.urlopen`, preserving existing caller behavior.
- Preconditions from source lines 7, 8, 9, 11-18, 19, 20, 22, 24, 25-27, 29-32, 33-36, 37, and 38-48 are documented and cited in tests.
