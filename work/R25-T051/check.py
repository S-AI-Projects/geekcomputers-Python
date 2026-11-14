import sys
from pathlib import Path

import pytest

TEST_FILE = Path(__file__).parent / "test_exception_handling.py"

if not TEST_FILE.exists():
    print(f"Test file not found: {TEST_FILE}", file=sys.stderr)
    sys.exit(1)

exit_code = pytest.main(["-v", str(TEST_FILE)])
sys.exit(int(exit_code))
