"""Regression tests locking down the contract and refactored behavior of checkBinod.

Contract & Preconditions:
    - Precondition Source Line 38: `with open(file, "r") as f:` requires a readable text file.
    - Precondition Source Line 40: `fileContent = f.read()` reads file contents.
    - Precondition Source Line 42: `has_binod = "binod" in fileContent.lower()`
    - Precondition Source Line 44: Emits confirmation message to stdout.
"""

import os
import sys
import unittest.mock as mock
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Mock time.sleep during module import to avoid top-level sleep delay
with mock.patch("time.sleep"):
    with mock.patch("builtins.print"):
        import binod


class TestCheckBinodContract:
    """Regression tests for checkBinod() before and after refactoring."""

    def test_smallest_valid_input_empty_file(self, tmp_path):
        """Smallest valid input: empty text file (0 bytes).

        Preconditions:
            - Source line 38 opens file.
            - Source line 40 reads empty content ("").
            - Source line 42 evaluates 'binod' in "" -> False.

        Input: empty file
        Expected: False
        """
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")

        result = binod.checkBinod(str(empty_file))
        assert result is False

    def test_ordinary_input_with_binod(self, tmp_path, capsys):
        """Ordinary input containing 'Binod'.

        Preconditions:
            - Source line 42 evaluates 'binod' in content.lower() -> True.
            - Source line 44 prints congratulations message.

        Input: 'Hello this is Binod checking in'
        Expected: True, prints message.
        """
        valid_file = tmp_path / "valid.txt"
        valid_file.write_text("Hello this is Binod checking in")

        result = binod.checkBinod(str(valid_file))
        assert result is True
        captured = capsys.readouterr()
        assert "Congratulations Binod found in" in captured.out

    def test_ordinary_input_without_binod(self, tmp_path, capsys):
        """Ordinary input without the keyword.

        Input: 'Just normal text'
        Expected: False, no congratulations printed.
        """
        file_without = tmp_path / "no_match.txt"
        file_without.write_text("Just normal text")

        result = binod.checkBinod(str(file_without))
        assert result is False
        captured = capsys.readouterr()
        assert "Congratulations Binod found in" not in captured.out

    def test_case_insensitivity_boundary(self, tmp_path):
        """Boundary: various capitalizations ('BINOD', 'bInOd', 'binod')."""
        for variant in ["BINOD", "bInOd", "binod"]:
            f = tmp_path / f"test_{variant}.txt"
            f.write_text(f"Text with {variant} present")
            assert binod.checkBinod(str(f)) is True
