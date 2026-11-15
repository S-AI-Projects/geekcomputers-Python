import importlib.util
import random
import subprocess
import sys
from pathlib import Path

import pytest


SOURCE = (
    Path(__file__).resolve().parents[2]
    / "Random Password Generator.py"
)
EXAMPLE = Path(__file__).with_name("example.py")


@pytest.fixture
def run_generator(monkeypatch, capsys):
    def execute(selected_characters):
        calls = []

        def fake_sample(population, k):
            calls.append((population, k))
            return selected_characters

        monkeypatch.setattr(random, "sample", fake_sample)

        spec = importlib.util.spec_from_file_location(
            "password_generator_test", SOURCE
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        output = capsys.readouterr().out
        return module, calls, output

    return execute


def test_smallest_valid_password_selection(run_generator):
    # Source lines 8-10 establish the pool and fixed length of 8.
    expected_pool = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*"
    )
    selected = list("abcdefgh")
    expected_password = "abcdefgh"

    module, calls, output = run_generator(selected)

    assert calls == [(expected_pool, 8)]
    assert module.password == expected_password
    assert output == expected_password + "\n"


def test_ordinary_password_selection(run_generator):
    # Source lines 8-10 establish the pool and fixed length of 8.
    expected_pool = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*"
    )
    selected = list("aB3!cD4@")
    expected_password = "aB3!cD4@"

    module, calls, output = run_generator(selected)

    assert calls == [(expected_pool, 8)]
    assert module.password == expected_password
    assert output == expected_password + "\n"
    assert len(module.password) == 8
    assert len(set(module.password)) == 8


def test_worked_example_displays_expected_output():
    result = subprocess.run(
        [sys.executable, str(EXAMPLE)],
        capture_output=True,
        text=True,
        check=True,
    )

    expected_output = (
        "Character pool size: 70\n"
        "Requested length: 8\n"
        "Selected characters: ['a', 'B', '3', '!', 'c', 'D', '4', '@']\n"
        "Final password: aB3!cD4@\n"
    )

    assert result.stdout == expected_output
    assert result.stderr == ""
