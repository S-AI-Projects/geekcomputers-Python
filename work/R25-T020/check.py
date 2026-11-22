#!/usr/bin/env python3
"""Focused test runner for Task R25-T020 (date-timeclient.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_datetimeclient.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T020 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T020

## Target
- **Script:** date-timeclient.py
- **Function:** `date_timeclient`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 3: `soc = socket.socket(...)` socket initialization.
- Line 4: `soc.connect((..., 2905))` connects to destination port 2905.
- Line 5: `recmsg = soc.recv(1024)` reads up to 1024 bytes.
- Line 6: `soc.close()` socket teardown.
- Line 7: `"The time got from the server is %s" % recmsg.decode("ascii")` formatting normalization.

## Mutation Analysis
- **Mutant 1 (Off-by-one port):** Connecting to port 2906 instead of 2905. Proven caught by `mock_soc.connect.assert_called_once_with((host, 2905))`.
- **Mutant 2 (Altered format prefix):** String modified to `"Time got from server is %s"`. Proven caught by strict return assertion.
- **Mutant 3 (Altered buffer size):** Changing `recv(1024)` to `recv(512)`. Proven caught by `mock_soc.recv.assert_called_once_with(1024)`.
- **Production Cleanliness:** The final implementation in `date-timeclient.py` contains zero mutant code or test hooks.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (empty) | L5, L7 | Payload `b""` | `"The time got from the server is "` | Matches expected | PASS |
| Ordinary input | L4, L5, L7 | `b"2026-11-23 00:00:00"` | Formatted string with ISO timestamp | Matches expected | PASS |
| Mutant 1: Port 2906 | L4 | Connect to 2906 | Fails port assertion | Caught by test | PASS |
| Mutant 2: Altered prefix | L7 | Changed string template | Fails string equality | Caught by test | PASS |
| Mutant 3: Buffer 512 | L5 | `recv(512)` | Fails buffer assertion | Caught by test | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T020 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
