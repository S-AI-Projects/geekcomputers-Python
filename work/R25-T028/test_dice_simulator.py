"""Failure-path and rejection behavior tests for start() in dice_rolling_simulator.py.

Contract & Preconditions:
    - Precondition Source Line 39: `input(">")` waits for Enter to proceed.
    - Precondition Source Line 55: `user_dice_chooser = input(">")` receives user input.
    - Precondition Source Line 57: `user_dice_chooser = int(user_dice_chooser)` parses integer.
    - Failure Source Line 57: Raises `ValueError` for non-integer inputs.
    - Rejection Source Line 71: `print("Please choose one of the applicable options!")`
    - Exit Source Line 107: `bye()` outputs farewell.
"""

import os
import random
import sys
import unittest.mock as mock
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import dice_rolling_simulator


class TestDiceRollingSimulatorFailurePaths:
    """Test suite covering failure, rejection, and recovery behaviors in start()."""

    def test_ordinary_valid_call(self, monkeypatch, capsys):
        """Ordinary input: user presses Enter, chooses 6, and exits.

        Inputs:
            Enter to start -> '6' -> 'exit'
        Expected:
            Rolled die value between 1 and 6, followed by farewell message.
        """
        inputs = iter(["", "6", "exit"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        monkeypatch.setattr(random, "randint", lambda a, b: 4)

        dice_rolling_simulator.start()

        captured = capsys.readouterr().out
        assert "Welcome to dice rolling simulator" in captured
        assert "You rolled a 4!" in captured
        assert "Thanks for using the Dice Rolling Simulator!" in captured

    def test_failure_path_non_numeric_input_raises_valueerror(self, monkeypatch):
        """Failure path: non-numeric input at dice selection raises ValueError at line 57.

        Smallest input reaching failure: empty string '' at dice prompt.
        Inputs:
            Enter to start -> '' (raises ValueError)
        """
        inputs = iter(["", ""])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

        with pytest.raises(ValueError) as excinfo:
            dice_rolling_simulator.start()

        assert "invalid literal for int()" in str(excinfo.value)

    def test_fallback_rejection_branch_and_recovery(self, monkeypatch, capsys):
        """Fallback rejection: user enters non-applicable integer (0), then recovers.

        Preconditions:
            - Source line 71: prints rejection message.
            - Retries result() and successfully processes '8' and exits.
        """
        inputs = iter(["", "0", "8", "exit"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        monkeypatch.setattr(random, "randint", lambda a, b: 7)

        dice_rolling_simulator.start()

        captured = capsys.readouterr().out
        assert "Please choose one of the applicable options!" in captured
        assert "You rolled a 7!" in captured
        assert "Thanks for using the Dice Rolling Simulator!" in captured

    def test_ordinary_valid_call_succeeds_after_failure(self, monkeypatch, capsys):
        """Verify that caller-owned state remains valid and a subsequent valid call succeeds."""
        # First: trigger failure
        bad_inputs = iter(["", "invalid_choice"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(bad_inputs))
        with pytest.raises(ValueError):
            dice_rolling_simulator.start()

        # Second: immediate subsequent valid call must succeed completely
        good_inputs = iter(["", "12", "exit"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(good_inputs))
        monkeypatch.setattr(random, "randint", lambda a, b: 11)

        dice_rolling_simulator.start()

        captured = capsys.readouterr().out
        assert "You rolled a 11!" in captured
        assert "Thanks for using the Dice Rolling Simulator!" in captured
