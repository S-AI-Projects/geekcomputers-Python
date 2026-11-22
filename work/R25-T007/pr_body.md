## Description
This pull request introduces a runnable worked example and focused regression tests for `ReadFromCSV.py`. It documents the decisive state transition—reading raw CSV file text from disk, parsing it into a structured pandas DataFrame, and projecting the column vectors `SalesID` and `ProductPrice` into discrete numeric coordinate lists `x` and `y` for plotting. It also allows optional headless visualization without blocking GUI event loops.

## Related Issue
Fixes: #12

## Type of Change
- [ ] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [x] Refactoring / Maintenance
- [ ] CI/CD

## Changes Made
- `ReadFromCSV.py`:
  - Modularized top-level script into `read_from_csv(filepath, show_plot=False)` (aliased to `ReadFromCSV`).
  - Added docstring explaining the contract, preconditions, and the decisive state transition.
  - Normalized column conversions to standard Python integers and floats via `.tolist()`.
  - Guarded interactive display in `main()` with `if __name__ == "__main__":`.
- `work/R25-T007/runnable_example.py`: Executable worked example script walking through file creation, DataFrame ingestion, coordinate extraction, and summary reporting.
- `work/R25-T007/test_read_from_csv.py`:
  - Tested smallest valid input (1-row CSV) asserting `x=[1]`, `y=[19.99]`.
  - Tested ordinary multi-row input asserting matching ordered pairs.
  - Executed `runnable_example.py` as a subprocess and verified displayed output assertions.
- `work/R25-T007/check.py`: Automated test runner exporting verification results.
- `work/R25-T007/RESULTS.md`: Detailed test results, cited source lines, and execution output.

## Screenshots / Recordings
N/A - CSV processing and data visualization backend logic.

## Testing
Executed local test runner:
```bash
python3 work/R25-T007/check.py
```
Output:
```
============================== 3 passed in 0.54s ===============================
All R25-T007 checks passed successfully.
```
Exit code: 0.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Preconditions cited directly from source lines:
- Line 2: `import pandas as pd` DataFrame ingestion library
- Line 11: `df = pd.read_csv(...)` CSV parsing
- Lines 12-14: `x = df['SalesID']` column extraction
- Line 15: `y = df['ProductPrice']` column extraction
- Lines 16-20: Matplotlib plotting configuration
