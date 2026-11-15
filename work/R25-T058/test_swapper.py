import importlib.util
from pathlib import Path

import pytest


SOURCE = Path(__file__).resolve().parents[2] / "swap.py"


@pytest.fixture
def swapper_module(monkeypatch):
    original_print = print

    # Suppress demonstration output only during module import.
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)

    spec = importlib.util.spec_from_file_location("swapper_test", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Restore normal print behavior for the actual tests.
    monkeypatch.setattr("builtins.print", original_print)

    return module


def test_smallest_invalid_input_raises_value_error(swapper_module):
    # Source lines 30-31: validation and ValueError branch.
    # Source lines 33-34: assignments occur only after validation.
    with pytest.raises(
        ValueError,
        match="Both x and y should be integers.",
    ):
        swapper_module.Swapper("a", 0)


def test_ordinary_invalid_input_raises_value_error(swapper_module):
    # Another invalid input: x is valid, y is a string.
    with pytest.raises(
        ValueError,
        match="Both x and y should be integers.",
    ):
        swapper_module.Swapper(5, "invalid")


def test_valid_object_survives_failed_construction_and_swaps(
    swapper_module, capsys
):
    # Source lines 33-34: initial state is x=5, y=10.
    # Source line 45: tuple unpacking should produce x=10, y=5.
    instance = swapper_module.Swapper(5, 10)

    with pytest.raises(ValueError):
        swapper_module.Swapper("a", 0)

    # Failed construction must not mutate the existing instance.
    assert instance.x == 5
    assert instance.y == 10

    instance.swap_tuple_unpacking()

    assert instance.x == 10
    assert instance.y == 5
    assert capsys.readouterr().out == (
        "Before swapping x: 5, y: 10\n"
        "After swapping x: 10, y: 5\n"
    )
