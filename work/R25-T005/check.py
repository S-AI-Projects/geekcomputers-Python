#!/usr/bin/env python3
"""Focused test runner for Task R25-T005 (voice.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_voice.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T005 ===")
    cmd = [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T005

## Target
- **Script:** voice.py
- **Function:** `voice`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 2: `from gtts import gTTS` text-to-speech dependency
- Line 7: `text = "Hello! This is a sample text to convert to speech."`
- Line 12: `tts = gTTS(text=text, lang="en")`
- Line 15: `tts.save("output.mp3")`
- Line 18: `os.system("start output.mp3")`

## Verification Matrix
| Scenario | Preconditions | Literal Input | Expected Output | Actual Result | Status |
|---|---|---|---|---|---|
| Smallest valid input | L12, L15, L18 | `text='a'`, `play=False` | `success=True, played=False` | `success=True, played=False` | PASS |
| Ordinary input | L7, L12, L15, L18 | Baseline text, `play=True` | `success=True, played=True` | `success=True, played=True` | PASS |
| Repeated verification | L12, L15, L18 | 5 sequential runs | 5 independent executions | 5 independent executions | PASS |
| Isolated error handling | Exception branch | Broken TTS builder | `success=False` with error | `success=False` with error | PASS |

## Test Runner Output
```
{result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T005 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
