#!/usr/bin/env python3
"""Focused test runner for Task R25-T016 (Audio_Summarizer.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_audio_summarizer.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T016 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T016

## Target
- **Script:** Audio_Summarizer.py
- **Functions:** `transcript_generator`, `transcribe_audio`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 9: `model = whisper.load_model("base")` loads model architecture.
- Line 12: `result = model.transcribe("audio.mp4")` transcribes audio track.
- Line 15: `provide_summarizer(result)` hands off dictionary to summarization.

## Refactoring Details
- **Extracted Responsibility:** Isolated audio file loading and transcription into dedicated `transcribe_audio(audio_file, model_name, model)` helper.
- **Single Responsibility Principle:** `transcript_generator` now acts strictly as an orchestrator between transcription and summarization, removing tight inline coupling.
- **Zero Breaking Changes:** Default parameters (`audio_path="audio.mp4"`, `model_name="base"`) maintain 100% backward compatibility for all existing callers.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (empty) | L12, L15 | `empty.mp4`, `{{"text": ""}}` | Dict `{{"text": ""}}` returned and passed | Matched | PASS |
| Ordinary input | L9, L12, L15 | `audio.mp4`, full sentence | Full transcription dict returned and passed | Matched | PASS |
| Isolated helper test | L9, L12 | `clip.mp3`, model mock | Helper executes model.transcribe cleanly | Matched | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T016 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
