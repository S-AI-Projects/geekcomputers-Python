import builtins
import importlib.util
from pathlib import Path

import pytest


SOURCE = (
    Path(__file__).resolve().parents[2]
    / "Type_of_angles_of_triangle.py"
)


def load_angle_module(monkeypatch, capsys, inputs):
    """Load the module while controlling import-time and test-time input."""
    values = iter(str(value) for value in inputs * 2)
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(values))

    spec = importlib.util.spec_from_file_location("angle_type_test", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # The first three inputs were consumed by the source's top-level call.
    capsys.readouterr()
    return module


def test_smallest_valid_acute_triangle(monkeypatch, capsys):
    # Source lines 18, 30, 42: read exactly three angles.
    # Independent expected result: 60 + 60 + 60 = 180; all are < 90.
    module = load_angle_module(monkeypatch, capsys, [60, 60, 60])

    result = module.angle_type()
    output = capsys.readouterr().out

    assert result is None
    assert "Acute Angle Triangle" in output
    assert "You have entered : [60, 60, 60]" in output


def test_ordinary_right_triangle(monkeypatch, capsys):
    # Source lines 18, 30, 42: read exactly three angles.
    # Independent expected result: 30 + 60 + 90 = 180; one angle is 90.
    module = load_angle_module(monkeypatch, capsys, [30, 60, 90])

    result = module.angle_type()
    output = capsys.readouterr().out

    assert result is None
    assert "Right Angle Triangle" in output
    assert "You have entered : [30, 60, 90]" in output


def test_invalid_angle_sum_returns_minus_one(monkeypatch, capsys):
    # Source lines 54-57: a sum other than 180 prints an error and returns -1.
    # Independent expected result: 60 + 60 + 30 = 150.
    module = load_angle_module(monkeypatch, capsys, [60, 60, 30])

    result = module.angle_type()
    output = capsys.readouterr().out

    assert result == -1
    assert "It is not a triangle!Please enter valid angles." in output
    assert "Acute Angle Triangle" not in output
    assert "Right Angle Triangle" not in output
    assert "Obtuse Angle triangle" not in output
