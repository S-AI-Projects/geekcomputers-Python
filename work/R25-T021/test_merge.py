"""Focused contract regression tests for merge() in merge.py.

Contract & Preconditions:
    - Precondition Source Line 18: Relies on module-level `resultfile` as output filename.
    - Precondition Source Lines 21-25: `csvfiles = [f for f in os.listdir(".") if f != resultfile and (len(f.split(".")) >= 2) and f.split(".")[1] == "csv"]`
      Scans current directory '.' for CSV files excluding resultfile.
    - Precondition Source Line 28: `with open(resultfile, "w") as writefile:`
      Opens resultfile in overwrite mode ('w').
    - Precondition Source Line 34: `writefile.write(readfile.read() + "\\n")`
      Appends read contents followed by newline.
"""

import os
import sys
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import merge


class TestMergeContract:
    """Regression test suite locking down the contract of merge.py:merge()."""

    def test_merge_smallest_valid_input_zero_csvs(self, monkeypatch, tmp_path):
        """Smallest valid input (zero candidate CSV files).

        Preconditions:
            - Source line 18 establishes destination filename `resultfile = "result.csv"`.
            - Source lines 21-25 filter files; with no CSVs, `csvfiles` evaluates to `[]`.
            - Source line 28 opens `resultfile` in write mode ("w").

        Inputs:
            Directory contains no .csv files.
        Expected outputs:
            - Return value: None (merge.py does not return a value).
            - Observable mutation: 'result.csv' created with length 0 bytes (empty string).
        """
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(merge, "resultfile", "result.csv")

        # Run merge
        return_value = merge.merge()

        # Separately assert return value and file mutation
        assert return_value is None, f"Expected return None, got {return_value}"
        result_path = tmp_path / "result.csv"
        assert result_path.exists(), "Expected result.csv to be created"
        actual_content = result_path.read_text()
        expected_content = ""
        assert actual_content == expected_content, (
            f"Expected empty content, got: {actual_content!r}"
        )

    def test_merge_smallest_valid_input_single_csv(self, monkeypatch, tmp_path):
        """Smallest valid input with content (single minimal CSV file).

        Preconditions:
            - Source lines 21-25 discover 'single.csv'.
            - Source lines 28-34 write read contents plus newline.

        Inputs:
            single.csv: "k,v\n1,2"
        Expected outputs:
            - Return value: None
            - Observable mutation: 'result.csv' contains "k,v\n1,2\n"
        """
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(merge, "resultfile", "result.csv")
        (tmp_path / "single.csv").write_text("k,v\n1,2")

        return_value = merge.merge()

        assert return_value is None
        result_file = tmp_path / "result.csv"
        assert result_file.exists()
        actual_content = result_file.read_text()
        expected_content = "k,v\n1,2\n"
        assert actual_content == expected_content

    def test_merge_ordinary_input(self, monkeypatch, tmp_path):
        """Ordinary input: two standard CSV files.

        Preconditions:
            - Source lines 21-25 discover 'a.csv' and 'b.csv'.
            - Source line 34 concatenates each file with a newline.

        Inputs:
            a.csv: "id,name\n1,Alpha"
            b.csv: "id,name\n2,Beta"
        Expected outputs:
            - Return value: None
            - Observable mutation: 'result.csv' contains both files' contents with trailing newlines.
        """
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(merge, "resultfile", "result.csv")
        (tmp_path / "a.csv").write_text("id,name\n1,Alpha")
        (tmp_path / "b.csv").write_text("id,name\n2,Beta")

        # Mock listdir order to ensure deterministic test execution across filesystems
        monkeypatch.setattr(os, "listdir", lambda path=".": ["a.csv", "b.csv"])

        return_value = merge.merge()

        assert return_value is None
        result_file = tmp_path / "result.csv"
        actual_content = result_file.read_text()
        expected_content = "id,name\n1,Alpha\nid,name\n2,Beta\n"
        assert actual_content == expected_content

    def test_merge_repeated_value_boundary(self, monkeypatch, tmp_path):
        """Repeated-value boundary: files with duplicate rows and identical contents.

        Preconditions:
            - Source lines 21-25 discover duplicate-content files.
            - Source line 34 writes all entries preserving duplicates (no deduplication).

        Inputs:
            rep1.csv: "val\n42\n42"
            rep2.csv: "val\n42\n42"
        Expected outputs:
            - Observable mutation: 'result.csv' preserves all duplicate values.
        """
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(merge, "resultfile", "result.csv")
        (tmp_path / "rep1.csv").write_text("val\n42\n42")
        (tmp_path / "rep2.csv").write_text("val\n42\n42")

        monkeypatch.setattr(os, "listdir", lambda path=".": ["rep1.csv", "rep2.csv"])

        return_value = merge.merge()

        assert return_value is None
        result_file = tmp_path / "result.csv"
        actual_content = result_file.read_text()
        expected_content = "val\n42\n42\nval\n42\n42\n"
        assert actual_content == expected_content

    def test_merge_ignores_non_csv_and_resultfile(self, monkeypatch, tmp_path):
        """Boundary test: non-CSV files and preexisting resultfile are excluded.

        Preconditions:
            - Source line 24 filters `f != resultfile and len(f.split('.')) >= 2 and f.split('.')[1] == 'csv'`.

        Inputs:
            result.csv: preexisting old content
            notes.txt: "not a csv"
            valid.csv: "col\n1"
        Expected outputs:
            - 'result.csv' is overwritten with only valid.csv's content ("col\n1\n").
        """
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(merge, "resultfile", "result.csv")
        (tmp_path / "result.csv").write_text("OLD_CONTENT")
        (tmp_path / "notes.txt").write_text("not a csv")
        (tmp_path / "valid.csv").write_text("col\n1")

        monkeypatch.setattr(os, "listdir", lambda path=".": ["result.csv", "notes.txt", "valid.csv"])

        return_value = merge.merge()

        assert return_value is None
        actual_content = (tmp_path / "result.csv").read_text()
        expected_content = "col\n1\n"
        assert actual_content == expected_content
