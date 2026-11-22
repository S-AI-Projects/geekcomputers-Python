#!/usr/bin/env python3
"""Focused test runner for R25-T036 — gcd.py refactoring checks.

Usage:
    python3 work/R25-T036/check.py

Runs focused Python tests using pytest.
Saves execution results and tool versions in work/R25-T036/.
Exits non-zero when any assertion fails.
"""

import os
import subprocess
import sys

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(TASK_DIR, "..", "..")
TEST_FILE = os.path.join(TASK_DIR, "test_gcd.py")
RESULTS_FILE = os.path.join(TASK_DIR, "results.txt")


def main():
    pytest_cmd = [sys.executable, "-m", "pytest", TEST_FILE, "-v", "--tb=short"]

    print("=" * 65)
    print("R25-T036 — gcd.py Refactoring Test Runner")
    print("=" * 65)
    print(f"Command: {' '.join(pytest_cmd)}")
    print(f"Test file: {TEST_FILE}")
    print(f"Target module: gcd.py")
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    print()

    result = subprocess.run(
        pytest_cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    # Count test results
    passed_count = 0
    failed_count = 0
    for line in result.stdout.splitlines():
        if " PASSED " in line:
            passed_count += 1
        elif " FAILED " in line:
            failed_count += 1

    total_tests = passed_count + failed_count

    # Save results to results.txt
    with open(RESULTS_FILE, "w") as f:
        f.write("R25-T036 — gcd.py Refactoring Test Results\n")
        f.write("=" * 60 + "\n")
        f.write(f"Command: {' '.join(pytest_cmd)}\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Exit code: {result.returncode}\n")
        f.write(f"Passed tests: {passed_count}\n")
        f.write(f"Failed tests: {failed_count}\n")
        f.write(f"Total test count: {total_tests}\n\n")
        f.write("--- stdout ---\n")
        f.write(result.stdout)
        if result.stderr:
            f.write("\n--- stderr ---\n")
            f.write(result.stderr)

    print(f"\nResults recorded to: {RESULTS_FILE}")
    print(f"Exit code: {result.returncode}")

    if result.returncode != 0:
        sys.exit(result.returncode)

    if total_tests == 0:
        print("ERROR: Non-zero test count required, but 0 tests were executed.")
        sys.exit(1)

    print("All R25-T036 checks PASSED.")
    sys.exit(0)


if __name__ == "__main__":
    main()
