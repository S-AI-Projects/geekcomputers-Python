## Description
This pull request measures and documents the computational complexity and scaling behavior of `webcam` in `webcam.py`. It extracts frame color conversion into a reusable function, adds explicit complexity documentation defining input size $N$ (total pixel count) with $O(N)$ asymptotic scaling, isolates algorithmic work from external camera driver/GUI I/O, and provides regression tests covering small fixtures and a multi-size scaling benchmark.

## Related Issue
Fixes: #23

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
- `webcam.py`:
  - Structured frame processing into `webcam(frames, color_conv=None)`.
  - Added docstring detailing input-size variable $N = W \times H \times \text{frames}$, $O(N)$ time/space complexity, and the boundary separating algorithmic computation from hardware/OS latency.
  - Safe import guards for optional dependencies (`cv2`, `colorama`).
  - Guarded infinite camera loop under `if __name__ == '__main__':`.
- `work/R25-T019/test_webcam.py`:
  - Tested smallest valid input ($1 \times 1$ pixel frame).
  - Tested ordinary input ($2 \times 2$ pixel frame).
  - Executed scaling experiment across 3 dimensions ($10\times 10$, $25\times 25$, $50\times 50$) with 5 repetitions each and deterministic random seed (seed=42).
  - Verified correctness of all outputs outside timed intervals without brittle wall-clock assertions.
- `work/R25-T019/check.py`: Automated test runner executing regression checks and generating verification receipts.
- `work/R25-T019/RESULTS.md`: Detailed test results matrix, timing distributions, and precondition citations.

## Screenshots / Recordings
N/A - Video frame processing complexity and unit tests.

## Testing
Executed automated test runner:
```bash
python3 work/R25-T019/check.py
```
Output:
```
Ran 3 tests in 0.007s
OK
All R25-T019 checks passed successfully.
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
- Lines 11-12: `frames_width`, `frames_height` resolution anchors
- Line 34: `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)` frame processing anchor.
