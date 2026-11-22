## Description
This pull request modularizes `voice.py` into a testable `voice(...)` function with dependency injection for the text-to-speech synthesizer (`gTTS`) and system command executor (`os.system`). This allows the speech synthesis workflow to be verified repeatably without network access, external audio drivers, or live GUI interaction.

## Related Issue
Fixes: #10

## Type of Change
- [ ] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [x] Refactoring / Maintenance
- [ ] CI/CD

## Changes Made
- `voice.py`:
  - Refactored top-level script into a function `voice(text, lang, output_file, play, tts_builder, system_executor)`.
  - Added dependency injection parameters with defaults preserving existing caller behavior.
  - Added contract docstring citing baseline preconditions and return structures.
  - Guarded interactive execution under `if __name__ == "__main__":`.
- `work/R25-T005/test_voice.py`:
  - Created mock TTS factory and mock system executor to isolate tests from network and OS dependencies.
  - Tested smallest valid input (`text="a"` with `play=False`).
  - Tested ordinary input (`"Hello! This is a sample text to convert to speech."` with playback).
  - Verified repeatable invocation and state isolation across multiple sequential executions.
  - Tested graceful error handling when synthesis fails.
- `work/R25-T005/check.py`: Automated test runner producing execution receipts.
- `work/R25-T005/RESULTS.md`: Complete verification report and precondition citations.

## Screenshots / Recordings
N/A - backend text-to-speech utility and unit tests.

## Testing
Executed local test runner:
```bash
python3 work/R25-T005/check.py
```
Output:
```
============================== 4 passed in 0.02s ===============================
All R25-T005 checks passed successfully.
```
Exit code: 0.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Preconditions cited directly from source lines:
- Line 2: `gTTS` library import
- Line 7: Baseline text definition
- Line 12: TTS object instantiation
- Line 15: File save operation
- Line 18: System audio playback command
