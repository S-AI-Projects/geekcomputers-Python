## Description
This pull request refactors `PONG_GAME.py` by simplifying the responsibilities inside `spawn_ball`. Specifically, the velocity vector derivation (speed calculation and directional sign mapping) is extracted into an independent helper `compute_ball_velocity`, decoupling mathematical calculation from global game-state resets (`ball_pos = [WIDTH / 2, HEIGHT / 2]`).

## Related Issue
Fixes: #11

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
- `PONG_GAME.py`:
  - Extracted velocity vector computation from `spawn_ball` into a focused helper `compute_ball_velocity(direction, rand_fn=None)`.
  - Added docstring explaining preconditions, bounds, and directional invariants.
  - Wrapped `simplegui` imports and GUI initialization so the game logic can run in headless CI and automated test environments.
- `work/R25-T006/test_pong.py`:
  - Verified smallest valid input (`direction=LEFT`) with expected ball centering `[300.0, 200.0]` and negative horizontal velocity.
  - Verified ordinary input (`direction=RIGHT`) with expected ball centering and positive horizontal velocity.
  - Added deterministic tests for `compute_ball_velocity` using mock random generators.
  - Verified that `spawn_ball` reliably resets corrupted initial ball coordinates.
- `work/R25-T006/check.py`: Automated test runner producing verification logs.
- `work/R25-T006/RESULTS.md`: Detailed test results and precondition citations.

## Screenshots / Recordings
N/A - 2D game logic refactoring and unit tests.

## Testing
Executed local test runner:
```bash
python3 work/R25-T006/check.py
```
Output:
```
============================== 4 passed in 0.02s ===============================
All R25-T006 checks passed successfully.
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
- Lines 7-8: Canvas dimensions `WIDTH = 600`, `HEIGHT = 400`
- Lines 14-15: Direction constants `LEFT = False`, `RIGHT = True`
- Line 26: Center reset `ball_pos = [WIDTH / 2, HEIGHT / 2]`
- Lines 28, 30: Velocity speed range calculations
