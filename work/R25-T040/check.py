"""check.py – focused test runner for R25-T040.

Runs the test suite and mutation verification for 'automail.py'.
Exits non-zero on any failure.

Usage:
    python3 work/R25-T040/check.py
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_FILE = Path(__file__).resolve().parent / "test_automail.py"


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"],
        cwd=str(REPO_ROOT),
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
