
import builtins
import importlib.util
import random
import string
import sys
import types
from pathlib import Path

import pytest


SOURCE = Path(__file__).resolve().parents[2] / "HangMan Game.py"

CASE_RANDOM = random.Random(2026)
GENERATED_NAMES = [
    "".join(
        CASE_RANDOM.choice(string.ascii_uppercase)
        for _ in range(CASE_RANDOM.randint(1, 12))
    )
    for _ in range(100)
]


def mock_includes(monkeypatch, secret_name):
    includes = types.ModuleType("HangMan_Includes")
    includes.names = [secret_name]
    includes.draw = [""] * 7
    includes.won = "WON"
    includes.lose = "LOST"

    monkeypatch.setitem(sys.modules, "HangMan_Includes", includes)
    monkeypatch.setattr(random, "choice", lambda names: secret_name)


def run_game(monkeypatch, inputs, secret_name="ANNA"):
    mock_includes(monkeypatch, secret_name)

    answers = iter(inputs)

    def controlled_input(prompt=""):
        try:
            return next(answers)
        except StopIteration:
            return "0"

    monkeypatch.setattr(builtins, "input", controlled_input)

    output = []
    monkeypatch.setattr(
        builtins,
        "print",
        lambda *args, **kwargs: output.append(
            " ".join(str(arg) for arg in args)
        ),
    )

    spec = importlib.util.spec_from_file_location("hangman_under_test", SOURCE)
    module = importlib.util.module_from_spec(spec)

    with pytest.raises(SystemExit):
        spec.loader.exec_module(module)

    return "\n".join(output)


class StopAtFirstGuess(Exception):
    pass


def capture_initial_display(monkeypatch, secret_name):
    mock_includes(monkeypatch, secret_name)

    output = []
    monkeypatch.setattr(
        builtins,
        "print",
        lambda *args, **kwargs: output.append(
            " ".join(str(arg) for arg in args)
        ),
    )

    def stop_before_guess(prompt=""):
        raise StopAtFirstGuess

    monkeypatch.setattr(builtins, "input", stop_before_guess)

    spec = importlib.util.spec_from_file_location(
        "hangman_initial_test", SOURCE
    )
    module = importlib.util.module_from_spec(spec)

    with pytest.raises(StopAtFirstGuess):
        spec.loader.exec_module(module)

    return "\n".join(output)


def test_initial_display_has_one_placeholder_per_character(monkeypatch):
    output = capture_initial_display(monkeypatch, "ANNA")

    assert "You have to Guess a Human Name of 4 Alphabets" in output
    assert "__ __ __ __" in output


def test_correct_letter_reveals_all_occurrences(monkeypatch):
    output = run_game(monkeypatch, ["A", "N", "0"], "ANNA")

    assert "A __ __ A" in output


def test_repeated_guess_is_reported(monkeypatch):
    output = run_game(monkeypatch, ["A", "A", "N", "0"], "ANNA")

    assert "Already Tried" in output


def test_correct_guess_does_not_reduce_chances(monkeypatch):
    output = run_game(monkeypatch, ["A", "N", "0"], "ANNA")

    assert "You were left with" not in output


@pytest.mark.parametrize("name", GENERATED_NAMES)
def test_initial_placeholder_count_matches_name_length(monkeypatch, name):
    output = capture_initial_display(monkeypatch, name)

    expected_display = "__ " * len(name)
    assert f"\t{expected_display}" in output
