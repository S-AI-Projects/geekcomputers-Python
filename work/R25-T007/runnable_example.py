#!/usr/bin/env python3
"""Runnable worked example for ReadFromCSV (R25-T007).

Demonstrates the step-by-step decisive state transition:
1. Raw CSV file ingestion into DataFrame.
2. Extraction of 'SalesID' into x coordinates and 'ProductPrice' into y coordinates.
3. Summary of coordinate pairs ready for plotting.
"""

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import ReadFromCSV as reader


def run_worked_example():
    # Step 1: Create a temporary CSV representing sales transactions
    csv_content = "SalesID,ProductPrice\n101,45.50\n102,60.00\n103,32.75\n"
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_csv = f.name

    print("Step 1: Input CSV Written")
    print(csv_content.strip())

    # Step 2: Execute ReadFromCSV without GUI blocking
    result = reader.read_from_csv(temp_csv, show_plot=False)

    # Step 3: Inspect intermediate DataFrame state
    print("\nStep 2: Intermediate DataFrame State")
    print(result["df"].to_string(index=False))

    # Step 4: Inspect extracted x and y coordinate arrays
    print("\nStep 3: Extracted Coordinate Series")
    print(f"X (SalesID): {result['x']}")
    print(f"Y (ProductPrice): {result['y']}")

    Path(temp_csv).unlink(missing_ok=True)
    return result


if __name__ == "__main__":
    run_worked_example()
