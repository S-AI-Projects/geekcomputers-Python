"""Focused regression tests for spawn_ball and compute_ball_velocity in PONG_GAME.py.

Precondition citations:
    - Source Lines 7-8: `WIDTH = 600`, `HEIGHT = 400`
    - Source Lines 14-15: `LEFT = False`, `RIGHT = True`
    - Source Line 26: `ball_pos = [WIDTH / 2, HEIGHT / 2]` establishes center position [300.0, 200.0]
    - Source Lines 28, 30: Velocity ranges [120..240]/60 for horizontal and [60..180]/60 for vertical
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import PONG_GAME as pong


class TestPongSpawnBall:
    """Tests verifying spawn_ball behavior, position resetting, and velocity calculation."""

    def test_smallest_valid_input_left(self):
        """Smallest valid input: direction LEFT (False).

        Preconditions:
            - Line 7-8: WIDTH=600, HEIGHT=400 -> center is [300.0, 200.0].
            - Line 14: LEFT = False.
            - Line 26: ball_pos = [WIDTH / 2, HEIGHT / 2].
            - Line 30: ball_vel[0] < 0 (moving leftwards).
        Literal input:
            direction = False (LEFT)
        Independently calculated expected output:
            ball_pos == [300.0, 200.0]
            -4.0 <= ball_vel[0] <= -2.0
            1.0 <= ball_vel[1] <= 3.0
        """
        pong.spawn_ball(pong.LEFT)

        assert pong.ball_pos == [300.0, 200.0], f"Expected [300.0, 200.0], got {pong.ball_pos}"
        vx, vy = pong.ball_vel
        assert -4.0 <= vx <= -2.0, f"Expected vx in [-4.0, -2.0], got {vx}"
        assert 1.0 <= vy <= 3.0, f"Expected vy in [1.0, 3.0], got {vy}"

    def test_ordinary_input_right(self):
        """Ordinary input: direction RIGHT (True).

        Preconditions:
            - Line 15: RIGHT = True.
            - Line 26: ball_pos = [WIDTH / 2, HEIGHT / 2].
            - Line 28: ball_vel[0] > 0 (moving rightwards).
        Literal input:
            direction = True (RIGHT)
        Independently calculated expected output:
            ball_pos == [300.0, 200.0]
            2.0 <= ball_vel[0] <= 4.0
            1.0 <= ball_vel[1] <= 3.0
        """
        pong.spawn_ball(pong.RIGHT)

        assert pong.ball_pos == [300.0, 200.0]
        vx, vy = pong.ball_vel
        assert 2.0 <= vx <= 4.0, f"Expected vx in [2.0, 4.0], got {vx}"
        assert 1.0 <= vy <= 3.0, f"Expected vy in [1.0, 3.0], got {vy}"

    def test_simplified_velocity_responsibility(self):
        """Tests the extracted compute_ball_velocity helper under deterministic mock PRNG."""
        # Mock generator returning predictable values: 180 for horiz, 120 for vert
        def mock_rand(low, high):
            return 180 if low == 120 else 120

        vel_right = pong.compute_ball_velocity(pong.RIGHT, rand_fn=mock_rand)
        assert vel_right == [3.0, 2.0], f"Expected [3.0, 2.0], got {vel_right}"

        vel_left = pong.compute_ball_velocity(pong.LEFT, rand_fn=mock_rand)
        assert vel_left == [-3.0, 2.0], f"Expected [-3.0, 2.0], got {vel_left}"

    def test_state_reset_contract(self):
        """Verifies that spawn_ball resets ball_pos regardless of prior corrupted ball position."""
        pong.ball_pos = [999.0, 999.0]
        pong.spawn_ball(pong.RIGHT)
        assert pong.ball_pos == [300.0, 200.0]
