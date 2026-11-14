
import builtins
import contextlib
import io
import runpy
from unittest.mock import patch
import ast
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2] / "Exception_Handling_in_Python.py"


def get_list_fixture():
    """Read the list fixture directly from the original source."""
    tree = ast.parse(SOURCE.read_text())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(
                isinstance(target, ast.Name) and target.id == "l"
                for target in node.targets
            ):
                return ast.literal_eval(node.value)

    raise AssertionError("List fixture 'l' was not found")

# Source: Exception_Handling_in_Python.py, line 70
# Fixture: l = [1, 2, 3, 4]

def test_smallest_valid_index():
    items = get_list_fixture()
    assert items[0] == 1


def test_ordinary_index():
    items = get_list_fixture()
    assert items[2] == 3


def test_last_valid_index():
    items = get_list_fixture()
    assert items[3] == 4

# Source: Exception_Handling_in_Python.py, lines 70, 73, 75
# Fixture, invalid index access and IndexError handler.

def test_out_of_range_index():
    items = get_list_fixture()

    try:
        items[4]
    except IndexError:
        actual = "IndexError"
    else:
        actual = "No exception"

    assert actual == "IndexError"

# Additional boundary input: [1, 1, 2, 2].
# This is an independently supplied test input, not the source fixture.

def test_repeated_value_index():
    items = [1, 1, 2, 2]
    assert items[1] == 1


def test_indexing_does_not_mutate_list():
    items = get_list_fixture()
    original = [1, 2, 3, 4]

    _ = items[2]

    assert items == original


def test_original_script_handles_index_error_and_final_exception():
    output = io.StringIO()
    fake_file = io.StringIO()

    def mocked_open(filename, mode="r", *args, **kwargs):
        if filename == "aaa.txt" and mode == "w":
            return fake_file
        if filename == "abc.txt" and mode == "r":
            raise FileNotFoundError(filename)
        raise AssertionError(f"Unexpected file operation: {filename}, {mode}")

    with (
        patch.object(builtins, "open", side_effect=mocked_open),
        contextlib.redirect_stdout(output),
    ):
        try:
            runpy.run_path(str(SOURCE))
        except Exception as error:
            assert str(error) == "You are legally underage!!!"
        else:
            raise AssertionError("Expected the final custom exception")

    assert (
        "Index of the sequence is out of range. "
        "Indexing in python starts from 0."
    ) in output.getvalue()
    assert "Incorrect file name used" in output.getvalue()
    assert "Hope all errors were resolved!!" in output.getvalue()
    assert fake_file.closed

