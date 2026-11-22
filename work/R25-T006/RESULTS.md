# Verification Evidence — R25-T006

## Target
- **Script:** PONG_GAME.py
- **Functions:** `spawn_ball`, `compute_ball_velocity`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest /Users/krishna/SnAIproject/work/R25-T006/test_pong.py -v --tb=short`

## Precondition Citations
- Lines 7-8: `WIDTH = 600`, `HEIGHT = 400`
- Lines 14-15: `LEFT = False`, `RIGHT = True`
- Line 26: `ball_pos = [WIDTH / 2, HEIGHT / 2]`
- Lines 28, 30: Velocity speed range calculations `randrange(120, 240) / 60` and `randrange(60, 180) / 60`

## Refactoring Summary
- **Extracted Responsibility:** Isolated initial launch velocity computation into `compute_ball_velocity(direction, rand_fn=None)`.
- **Decoupling Benefit:** Separates state reset (setting global coordinates to `[WIDTH/2, HEIGHT/2]`) from mathematical vector scaling and directional negation.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest input (direction LEFT) | L7-8, L14, L26, L30 | `direction=False` | `ball_pos=[300, 200]`, `vx in [-4, -2]`, `vy in [1, 3]` | `ball_pos=[300, 200]`, `vx in [-4, -2]`, `vy in [1, 3]` | PASS |
| Ordinary input (direction RIGHT) | L7-8, L15, L26, L28 | `direction=True` | `ball_pos=[300, 200]`, `vx in [2, 4]`, `vy in [1, 3]` | `ball_pos=[300, 200]`, `vx in [2, 4]`, `vy in [1, 3]` | PASS |
| Deterministic velocity calculation | L28, L30 | Mock rand returning 180/120 | `RIGHT -> [3.0, 2.0]`, `LEFT -> [-3.0, 2.0]` | `RIGHT -> [3.0, 2.0]`, `LEFT -> [-3.0, 2.0]` | PASS |
| Position reset invariant | L26 | Prior `ball_pos=[999, 999]` | `ball_pos=[300, 200]` | `ball_pos=[300, 200]` | PASS |

## Test Runner Output
```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.14/bin/python3
cachedir: .pytest_cache
rootdir: /Users/krishna/SnAIproject
collecting ... collected 4 items

work/R25-T006/test_pong.py::TestPongSpawnBall::test_smallest_valid_input_left PASSED [ 25%]
work/R25-T006/test_pong.py::TestPongSpawnBall::test_ordinary_input_right PASSED [ 50%]
work/R25-T006/test_pong.py::TestPongSpawnBall::test_simplified_velocity_responsibility PASSED [ 75%]
work/R25-T006/test_pong.py::TestPongSpawnBall::test_state_reset_contract PASSED [100%]

============================== 4 passed in 0.02s ===============================
```

**Exit Code:** 0
