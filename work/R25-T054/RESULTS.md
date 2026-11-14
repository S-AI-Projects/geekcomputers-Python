# R25-T054 — HangMan Game Invariant Tests

## Target
- Source: `HangMan Game.py`
- Functionality tested: initial hidden-letter display and guessing behaviour.
- Original source file: unchanged.

## Source observations
- Line 9: selects a name from `incl.names` and converts it to uppercase.
- Line 11: creates one `"__ "` placeholder for each character in the name.
- Line 14: displays the name length and initial hidden-letter display.
- Lines 24–32: accept guesses and prevent repeated guesses.
- Lines 36–52: locate matching letters and reveal their positions.

## Test approach
The repository does not contain the imported `HangMan_Includes` dependency.
The tests provide a controlled mock module with a deterministic name and
mocked drawing strings. Input and output are also mocked so the game does
not require interactive terminal input.

Four focused tests check:
1. Initial display and placeholder count.
2. Revealing all occurrences of a correct letter.
3. Reporting a repeated guess.
4. Correct guesses not reducing the remaining chances.

A further 100 deterministic cases check the initial placeholder count.
The generated uppercase strings have lengths from 1 to 12 and use
a fixed random seed of 2026.

## Execution environment
- Python: 3.12.16
- pytest: 9.2.0
- Command: `python work/R25-T054/check.py`

## Normal test result
104 passed in 0.04s.

A subsequent verification after mutation testing also passed:
104 passed in 0.07s.

## Mutation test
A temporary copy of the source was created with the placeholder loop
changed from `range(len(name))` to `range(len(name) - 1)`.

The generated invariant tests detected the defect:
100 failed, 4 deselected.

The original test file was restored, and the normal suite passed again.
The original `HangMan Game.py` was not modified.

## Files
- `check.py`: focused pytest runner.
- `test_hangman.py`: regression and generated invariant tests.
- `RESULTS.md`: test method, environment, and evidence.
