#!/usr/bin/env python3
"""Focused test runner for R25-T032 — simpleInterest boundary checks.

Usage:
    python3 work/R25-T032/check.py

Runs the boundary tests for simpleInterest() using pytest.
Exits non-zero when any assertion fails.
"""

import subprocess
import sys
import os

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(TASK_DIR, "..", "..")
TEST_FILE = os.path.join(TASK_DIR, "test_simple_interest.py")
RESULTS_FILE = os.path.join(TASK_DIR, "results.txt")


def main():
    # Determine pytest command
    pytest_cmd = [sys.executable, "-m", "pytest", TEST_FILE, "-v", "--tb=short"]

    print(f"=" * 60)
    print(f"R25-T032 — simpleInterest Boundary Check Runner")
    print(f"=" * 60)
    print(f"Command: {' '.join(pytest_cmd)}")
    print(f"Test file: {TEST_FILE}")
    print(f"Target module: simpleInterest.py")
    print()

    # Run pytest
    result = subprocess.run(
        pytest_cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    # Print output
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    # Count tests from output
    test_count = 0
    for line in result.stdout.splitlines():
        if line.strip().startswith("test_") or "PASSED" in line or "FAILED" in line:
            test_count += 1

    # Save results
    with open(RESULTS_FILE, "w") as f:
        f.write(f"R25-T032 — simpleInterest Boundary Check Results\n")
        f.write(f"{'=' * 50}\n")
        f.write(f"Command: {' '.join(pytest_cmd)}\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Exit code: {result.returncode}\n")
        f.write(f"Test count (non-zero): {test_count}\n\n")
        f.write(f"--- stdout ---\n{result.stdout}\n")
        if result.stderr:
            f.write(f"--- stderr ---\n{result.stderr}\n")

    print(f"\nResults saved to: {RESULTS_FILE}")
    print(f"Exit code: {result.returncode}")

    # Propagate failure
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
