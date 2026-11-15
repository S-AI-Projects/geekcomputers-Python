# R25-T060 — Strengthen the tests of threading()

## Objective

Verify that `threading()` creates a worker thread targeting `download`,
starts that thread exactly once, and preserves its public return behavior.

Demonstrate that the regression tests detect a plausible one-line mistake.

## Source inspection and line anchors

File: `youtubedownloader.py`

- Line 7: defines `threading()` with no arguments.
- Line 9: constructs `Thread(target=download)`.
- Line 10: starts the created thread.
- Line 13: defines the worker function `download()`.
- Lines 29–30: protect GUI startup with the main-module guard.

The function has no input parameters and implicitly returns `None`.
It does not mutate caller-owned data. Its observable behavior is creating
and starting a worker thread.

## Test cases

Because the public function takes no arguments, the smallest valid call
and the ordinary repeated-call case both use its documented no-argument
interface.

### 1. Smallest valid call

Input:

    threading()

Expected:

- Return value is `None`.
- Exactly one thread is created.
- Its target is the module's `download` function.
- Its `start()` method is called exactly once.

Actual: all assertions passed.

Source anchors: lines 7, 9–10.

### 2. Ordinary repeated call

Inputs:

    threading()
    threading()

Expected:

- Both calls return `None`.
- Two distinct thread objects are created.
- Both target the `download` function.
- Each thread is started exactly once.

Actual: all assertions passed.

Source anchors: lines 9–10.

## Test isolation

- Only `youtubedownloader.py` is imported.
- Tkinter and pytube imports are stubbed.
- `Thread` is replaced with a deterministic fake.
- No real background thread is started.
- No GUI, YouTube request, or external I/O is performed.

## Mutation experiment

A temporary copy of the source was changed with one mutation:

Original:

    t1 = Thread(target=download)

Mutant:

    t1 = Thread(target=None)

The repository's original source file was not modified.

The same named regression tests were executed against the temporary mutant.

Expected behavior:

- Original implementation passes.
- Mutant fails the assertion that the thread target is `download`.

Actual mutant result:

    2 failed

Both tests failed at the target identity assertion:

    assert created[0].target is downloader_module.download

The actual target was `None`, while the expected target was the `download`
function. This is a semantic failure, not a timing or environment failure.

The mutation checker confirmed that the expected assertion failure occurred:

    SUCCESS: The regression tests detected the one-line mutation.

## Verification

Original implementation command:

    python3 work/R25-T060/check.py

Actual result:

    2 passed in 0.04s

Mutation experiment command:

    python3 work/R25-T060/mutation_check.py

Actual result:

    Mutant test exit code: 1
    2 failed
    SUCCESS: The regression tests detected the one-line mutation.

Environment:

- Python 3.12.16
- pytest 9.2.0

## Deliverables

- `test_threading.py` — deterministic threading regression tests
- `mutation_check.py` — temporary one-line mutation experiment
- `check.py` — focused test runner
- `RESULTS.md` — source anchors, expected behavior, and verification evidence

The original `youtubedownloader.py` implementation remains unchanged.
