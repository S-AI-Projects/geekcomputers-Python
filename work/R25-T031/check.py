#!/usr/bin/env python3
"""Automated focused test runner for R25-T031 (recursive-fibonacci.py).

Executes focused regression tests using the project configuration / pytest,
propagates test failures with non-zero exit codes, and reports test results.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEST_FILE = ROOT / "work" / "R25-T031" / "test_recursive_fibonacci.py"


def main():
    if not TEST_FILE.exists():
        print(f"Error: Test file not found: {TEST_FILE}", file=sys.stderr)
        return 1

    # Check for pytest availability
    pytest_bin = None
    try:
        import pytest  # noqa: F401
        pytest_cmd = [sys.executable, "-m", "pytest", "-v", str(TEST_FILE)]
    except ImportError:
        venv_pytest = ROOT / ".venv" / "bin" / "pytest"
        if venv_pytest.exists():
            pytest_cmd = [str(venv_pytest), "-v", str(TEST_FILE)]
        else:
            # Fallback to direct Python runner in test file
            pytest_cmd = [sys.executable, str(TEST_FILE)]

    print(f"Executing check command: {' '.join(pytest_cmd)}")
    result = subprocess.run(pytest_cmd, cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

