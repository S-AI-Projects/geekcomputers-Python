## Description
This pull request defines and tests the supported boundary domain of `polygon` in `polygon.py`. It establishes the geometric minimum vertex boundary (`len(points) >= 3` for valid 2D planar polygons), provides explicit guards for unsupported vertex counts (< 3), preserves source color anchors (`WHITE` and `GREEN`), and wraps the interactive GUI event loop so the module can be imported cleanly and safely in automated testing and CI environments.

## Related Issue
Fixes: #16

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
- `polygon.py`:
  - Structured polygon rendering into a reusable `polygon(surface=None, color=GREEN, points=...)` function.
  - Documented supported domain and boundary behavior in docstrings with citations to line anchors.
  - Added boundary validation: raises `ValueError` if fewer than 3 points are supplied.
  - Protected pygame initialization and interactive loop under `if __name__ == '__main__':` for headless safety.
- `work/R25-T012/test_polygon.py`:
  - Tested smallest supported boundary input (minimal 3-point triangle `((0, 0), (1, 0), (0, 1))`).
  - Tested ordinary canonical input (`((146, 0), (236, 277), (56, 277))`).
  - Tested ordinary interior input (4-point quadrilateral).
  - Tested unsupported boundary inputs (2-point segment and empty points tuple) asserting `ValueError`.
  - Asserted preservation of source color anchors `WHITE` and `GREEN`.
- `work/R25-T012/check.py`: Automated test runner executing boundary checks and generating verification receipts.
- `work/R25-T012/RESULTS.md`: Detailed test results matrix, boundary partitioning table, and precondition citations.

## Screenshots / Recordings
N/A - Planar polygon geometry validation and unit tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T012/check.py
```
Output:
```
Ran 6 tests in 0.001s
OK
All R25-T012 checks passed successfully.
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
- Line 9: `WHITE = (255, 255, 255)` color anchor
- Line 10: `GREEN = (0, 255, 0)` color anchor
- Line 13: `pygame.draw.polygon(window, GREEN, ((146, 0), (236, 277), (56, 277)))` default call
- Planar geometry boundary: minimal polygon boundary at 3 vertices.
