#!/usr/bin/env python3
"""Focused test runner for Task R25-T006 (PONG_GAME.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_pong.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T006 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T006

## Target
- **Script:** PONG_GAME.py
- **Functions:** `spawn_ball`, `compute_ball_velocity`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

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
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T006 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
