
import builtins
import importlib.util
import sys
import types
from pathlib import Path

import pytest


SOURCE = (
    Path(__file__).resolve().parents[2]
    / "Voice Command Calculator.py"
)


@pytest.fixture
def calculator_module(monkeypatch):
    """Load the calculator while mocking microphone and speech recognition."""

    speech = types.ModuleType("speech_recognition")
    speech.__version__ = "test"

    class FakeRecognizer:
        def adjust_for_ambient_noise(self, source):
            pass

        def listen(self, source):
            return object()

        def recognize_google(self, audio):
            return "1 + 1"

    class FakeMicrophone:
        def __init__(self, device_index=None):
            self.device_index = device_index

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    speech.Recognizer = FakeRecognizer
    speech.Microphone = FakeMicrophone

    monkeypatch.setitem(sys.modules, "speech_recognition", speech)
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)

    spec = importlib.util.spec_from_file_location(
        "voice_calculator_test", SOURCE
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def test_smallest_valid_addition_is_repeatable(calculator_module):
    # Source line 33 converts both operands to integers before evaluation.
    op1, op2 = 0, 0
    expected = 0

    operation = calculator_module.get_operator_fn("+")

    assert callable(operation)
    assert operation(op1, op2) == expected
    assert operation(op1, op2) == expected
    assert (op1, op2) == (0, 0)


def test_ordinary_multiplication_isolated_from_other_calls(
    calculator_module,
):
    # Source line 33 converts both operands to integers before evaluation.
    op1, op2 = 7, 3
    expected = 21

    multiply = calculator_module.get_operator_fn("x")
    add = calculator_module.get_operator_fn("+")

    first_result = multiply(op1, op2)
    assert first_result == expected

    # An unrelated valid operation must not affect multiplication.
    assert add(0, 0) == 0

    second_result = multiply(op1, op2)
    assert second_result == expected
    assert first_result == second_result
    assert (op1, op2) == (7, 3)


def test_repeated_operator_lookup_returns_equivalent_behavior(
    calculator_module,
):
    first = calculator_module.get_operator_fn("+")
    second = calculator_module.get_operator_fn("+")

    assert first(4, 5) == 9
    assert second(4, 5) == 9
    assert first(4, 5) == second(4, 5)
