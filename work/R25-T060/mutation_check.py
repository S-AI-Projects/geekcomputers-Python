import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "youtubedownloader.py"
TEST_FILE = Path(__file__).with_name("test_threading.py")

original = SOURCE.read_text()
old_line = "t1 = Thread(target=download)"
mutated_line = "t1 = Thread(target=None)"

assert original.count(old_line) == 1, "Expected source line was not unique"

mutated = original.replace(old_line, mutated_line, 1)

with tempfile.TemporaryDirectory() as directory:
    mutant_path = Path(directory) / "youtubedownloader_mutant.py"
    mutant_path.write_text(mutated)

    environment = os.environ.copy()
    environment["T060_SOURCE_PATH"] = str(mutant_path)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(TEST_FILE), "-q"],
        capture_output=True,
        text=True,
        env=environment,
    )

    print("Temporary mutation: Thread(target=download) -> Thread(target=None)")
    print("Original source modified: No")
    print("Mutant test exit code:", result.returncode)
    print(result.stdout)

    if result.returncode == 0:
        raise SystemExit("ERROR: Tests unexpectedly passed against the mutant.")

    if "assert None is" not in result.stdout:
        print(result.stderr)
        raise SystemExit("ERROR: Failure did not show the expected target assertion.")

    print("SUCCESS: The regression tests detected the one-line mutation.")
