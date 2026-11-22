"""Focused tests for ReadFromCSV in ReadFromCSV.py, including worked example execution assertion.

Precondition citations:
    - Source Line 2: `import pandas as pd` loads DataFrame engine
    - Source Line 11: `df = pd.read_csv(...)` loads CSV table
    - Source Lines 12-14: `x = df['SalesID']` extracts SalesID column
    - Source Line 15: `y = df['ProductPrice']` extracts ProductPrice column
    - Source Lines 16-20: Plot axis labeling and rendering
"""

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import ReadFromCSV as reader


class TestReadFromCSVExample:
    """Validates inputs, intermediate state extraction, and worked example execution."""

    def test_smallest_valid_input_single_row(self, tmp_path):
        """Smallest valid input: single-row CSV table.

        Preconditions:
            - Line 11: pd.read_csv reads table with header and 1 row.
            - Line 12-14: x extracts [1].
            - Line 15: y extracts [19.99].
        Literal input:
            "SalesID,ProductPrice\\n1,19.99\\n"
        Independently calculated expected output:
            x == [1]
            y == [19.99]
        """
        csv_file = tmp_path / "single.csv"
        csv_file.write_text("SalesID,ProductPrice\n1,19.99\n", encoding="utf-8")

        res = reader.read_from_csv(str(csv_file), show_plot=False)

        assert res["x"] == [1], f"Expected [1], got {res['x']}"
        assert res["y"] == [19.99], f"Expected [19.99], got {res['y']}"
        assert len(res["df"]) == 1

        # Check alias
        alias_res = reader.ReadFromCSV(str(csv_file), show_plot=False)
        assert alias_res["x"] == res["x"]

    def test_ordinary_input_multi_row(self, tmp_path):
        """Ordinary input: multi-row CSV with 3 data points.

        Preconditions:
            - Line 11: Ingests 3 distinct sales records.
            - Lines 12-15: Extracts 3 ordered pairs matching rows.
        Literal input:
            "SalesID,ProductPrice\\n101,45.50\\n102,60.00\\n103,32.75\\n"
        Independently calculated expected output:
            x == [101, 102, 103]
            y == [45.50, 60.00, 32.75]
        """
        csv_file = tmp_path / "multi.csv"
        csv_file.write_text("SalesID,ProductPrice\n101,45.50\n102,60.00\n103,32.75\n", encoding="utf-8")

        res = reader.read_from_csv(str(csv_file), show_plot=False)

        assert res["x"] == [101, 102, 103]
        assert res["y"] == [45.50, 60.00, 32.75]
        assert len(res["df"]) == 3

    def test_worked_example_execution_and_stdout(self):
        """Executes work/R25-T007/runnable_example.py and asserts displayed output."""
        example_script = Path(__file__).parent / "runnable_example.py"
        run_res = subprocess.run(
            [sys.executable, str(example_script)],
            capture_output=True,
            text=True,
            check=True,
        )

        stdout = run_res.stdout
        # Assert decisive state transitions are documented in output
        assert "Step 1: Input CSV Written" in stdout
        assert "Step 2: Intermediate DataFrame State" in stdout
        assert "Step 3: Extracted Coordinate Series" in stdout
        assert "X (SalesID): [101, 102, 103]" in stdout
        assert "Y (ProductPrice): [45.5, 60.0, 32.75]" in stdout
