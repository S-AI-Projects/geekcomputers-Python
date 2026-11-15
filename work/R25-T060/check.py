from pathlib import Path
import pytest

TEST_FILE = Path(__file__).with_name("test_threading.py")

if __name__ == "__main__":
    raise SystemExit(pytest.main([str(TEST_FILE), "-q"]))
