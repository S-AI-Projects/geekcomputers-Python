"""Executable documentation and regression tests for generate_unique_name.

Contract & Preconditions:
    - Precondition Source Line 46: `base_name, extension = os.path.splitext(name)`
    - Precondition Source Line 47: `index = 1`
    - Precondition Source Line 48: `while os.path.exists(os.path.join(directory, f"{base_name}_{index}{extension}")):`
    - Precondition Source Line 49: `index += 1`
    - Precondition Source Line 50: `return f"{base_name}_{index}{extension}"`
"""

import doctest
import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import snake_case_renamer_depth_one
from snake_case_renamer_depth_one import generate_unique_name


class TestGenerateUniqueNameExecutableDocs:
    """Tests executing and validating documentation examples and edge cases."""

    def test_doctest_execution(self):
        """Execute the worked example embedded in generate_unique_name docstring."""
        results = doctest.testmod(snake_case_renamer_depth_one, verbose=True)
        assert results.failed == 0, f"Doctest failed: {results}"
        assert results.attempted >= 1, "At least one doctest must be executed"

    def test_docstring_worked_example_trace_and_decisive_transition(self, tmp_path):
        """Execute the docstring's worked example and verify the decisive state transition.

        Decisive State Transition:
            - Candidate 'report_1.txt' exists -> loop condition True -> index advances to 2.
            - Candidate 'report_2.txt' exists -> loop condition True -> index advances to 3.
            - Candidate 'report_3.txt' does not exist -> loop condition False (decisive exit).
        """
        # Setup colliding files as documented in the worked example
        file1 = tmp_path / "report_1.txt"
        file2 = tmp_path / "report_2.txt"
        file1.write_text("first")
        file2.write_text("second")

        # Verify intermediate filesystem states
        assert os.path.exists(os.path.join(tmp_path, "report_1.txt")) is True
        assert os.path.exists(os.path.join(tmp_path, "report_2.txt")) is True
        assert os.path.exists(os.path.join(tmp_path, "report_3.txt")) is False

        # Execute
        unique_name = generate_unique_name(str(tmp_path), "report.txt")

        # Assert output matches the documented example
        assert unique_name == "report_3.txt"

    def test_smallest_valid_input_empty_directory(self, tmp_path):
        """Smallest valid input: empty directory (0 collisions).

        Preconditions:
            - Source line 47 initializes index = 1.
            - Source line 48 evaluates os.path.exists for 'test_1.txt' -> False.
            - Source line 50 returns immediately with index = 1.

        Input: directory=empty, name='test.txt'
        Expected: 'test_1.txt'
        """
        literal_dir = str(tmp_path)
        literal_name = "test.txt"
        expected_output = "test_1.txt"

        actual_output = generate_unique_name(literal_dir, literal_name)
        assert actual_output == expected_output

    def test_smallest_input_filename_without_extension(self, tmp_path):
        """Smallest valid input without extension: single character 'a'.

        Preconditions:
            - Source line 46: splitext('a') -> ('a', '')
            - Source lines 47-50: returns 'a_1'
        """
        result = generate_unique_name(str(tmp_path), "a")
        assert result == "a_1"

    def test_ordinary_input_single_collision(self, tmp_path):
        """Ordinary input with a single existing file collision.

        Input: 'data_1.csv' exists on disk, requesting 'data.csv'.
        Expected: 'data_2.csv'
        """
        (tmp_path / "data_1.csv").write_text("id,val")
        result = generate_unique_name(str(tmp_path), "data.csv")
        assert result == "data_2.csv"
