#!/usr/bin/env python3
"""Focused test runner for R25-T033 — get_players cross-check.

Usage:
    python3 work/R25-T033/check.py

Runs the cross-check tests for get_players() using pytest.
Exits non-zero when any assertion fails.
"""

import subprocess
import sys
import os

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(TASK_DIR, "..", "..")
TEST_FILE = os.path.join(TASK_DIR, "test_get_players.py")
RESULTS_FILE = os.path.join(TASK_DIR, "results.txt")


def main():
    # Determine pytest command
    pytest_cmd = [sys.executable, "-m", "pytest", TEST_FILE, "-v", "--tb=short"]

    print("=" * 60)
    print("R25-T033 — get_players Cross-Check Runner")
    print("=" * 60)
    print(f"Command: {' '.join(pytest_cmd)}")
    print(f"Test file: {TEST_FILE}")
    print(f"Target module: RandomNumberGame.py")
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
        if "PASSED" in line or "FAILED" in line:
            test_count += 1

    # Save results
    with open(RESULTS_FILE, "w") as f:
        f.write("R25-T033 — get_players Cross-Check Results\n")
        f.write("=" * 50 + "\n")
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

