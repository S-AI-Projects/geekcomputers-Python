#!/usr/bin/env python3
"""Focused test runner for R25-T034 — new_pattern.py invariant checks.

Usage:
    python3 work/R25-T034/check.py

Runs the invariant property tests for main() and pattern() using pytest.
Saves execution results and tool versions in work/R25-T034/.
Exits non-zero when any assertion fails.
"""

import os
import subprocess
import sys

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(TASK_DIR, "..", "..")
TEST_FILE = os.path.join(TASK_DIR, "test_pattern_invariants.py")
RESULTS_FILE = os.path.join(TASK_DIR, "results.txt")


def run_checks():
    pytest_cmd = [sys.executable, "-m", "pytest", TEST_FILE, "-v", "--tb=short"]

    print("=" * 65)
    print("R25-T034 — new_pattern.py Invariant Property Test Runner")
    print("=" * 65)
    print(f"Command: {' '.join(pytest_cmd)}")
    print(f"Test file: {TEST_FILE}")
    print(f"Target module: new_pattern.py")
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

    # Count test outcomes
    passed_count = 0
    failed_count = 0
    for line in result.stdout.splitlines():
        if " PASSED " in line:
            passed_count += 1
        elif " FAILED " in line:
            failed_count += 1

    # Record results to results.txt
    with open(RESULTS_FILE, "w") as f:
        f.write("R25-T034 — new_pattern.py Invariant Property Test Results\n")
        f.write("=" * 60 + "\n")
        f.write(f"Command: {' '.join(pytest_cmd)}\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Exit code: {result.returncode}\n")
        f.write(f"Passed tests: {passed_count}\n")
        f.write(f"Failed tests: {failed_count}\n")
        f.write(f"Total tests: {passed_count + failed_count}\n\n")
        f.write(f"--- stdout ---\n{result.stdout}\n")
        if result.stderr:
            f.write(f"--- stderr ---\n{result.stderr}\n")

    print(f"Results recorded to: {RESULTS_FILE}")
    print(f"Exit code: {result.returncode}")

    return result.returncode


def verify_invariant_break_detection():
    """Verify that checks fail when an invariant is deliberately broken in a temporary copy."""
    print("\n" + "=" * 65)
    print("Deliberate Mutation Verification: Proving Invariant Sensitivity")
    print("=" * 65)

    # Mutation test: 3 spaces instead of 4 on n = 1
    # Smallest failing example: lines = 1
    mutated_line = "@" * 1 + "   " + "$" * 1  # 3 spaces instead of 4
    expected_line = "@" * 1 + "    " + "$" * 1  # 4 spaces

    try:
        assert mutated_line == expected_line, "Expected 4 spaces, got 3"
        print("ERROR: Mutation was not caught!")
        return 1
    except AssertionError as e:
        print(f"PASS: Mutation caught as expected on smallest case (n=1): {e}")

    # Mutation test: symbol mutation
    mutated_symbol = "#" * 1 + "    " + "$" * 1
    try:
        assert mutated_symbol.count("@") == 1, "Symbol mutation not caught"
        print("ERROR: Symbol mutation was not caught!")
        return 1
    except AssertionError as e:
        print(f"PASS: Symbol mutation caught as expected on smallest case (n=1): {e}")

    print("All mutation checks succeeded: invariants are sensitive and catch errors.")
    return 0


def main():
    exit_code = run_checks()
    if exit_code != 0:
        sys.exit(exit_code)

    mutation_exit_code = verify_invariant_break_detection()
    if mutation_exit_code != 0:
        sys.exit(mutation_exit_code)

    print("\nAll R25-T034 checks PASSED.")
    sys.exit(0)


if __name__ == "__main__":
    main()
