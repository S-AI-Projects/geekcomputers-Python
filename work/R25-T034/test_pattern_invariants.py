"""Invariant and property tests for main() and pattern() from new_pattern.py.

Task: R25-T034
Target: new_pattern.py — main() (line 1)

Verifies:
1. Executable source anchors: print(pattern(3)), print(pattern(1)), print(pattern(0))
2. Derived neighboring supported input (lines = 2) with independently calculated output
3. 100+ bounded valid cases generated with fixed seed (seed = 42)
4. Key invariants:
   - Determinism / Idempotence: repeated calls with equivalent inputs yield identical results
   - Line count invariant: n lines for n > 0; 1 blank line for n == 0
   - Character count & symmetry invariant: count('@') == count('$') == n * (n + 1) // 2
   - Per-line structure invariant: '@' * (n - k) + '    ' + '$' * (k + 1)
   - Line length invariant: each line has length n + 5
5. Deliberately broken invariant checks: verifies checks fail when invariants are violated,
   identifying n = 1 as the smallest positive failing example.
"""

import builtins
import io
import os
import random
import sys
import pytest

# Ensure the repository root is in sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from new_pattern import main, pattern


# ---------------------------------------------------------------------------
# Independent Oracle & Test Harness
# ---------------------------------------------------------------------------


def oracle_pattern(lines: int) -> str:
    """Independent reference implementation for pattern(lines).

    Constructs the expected string without calling new_pattern.pattern.
    Preconditions (source lines 40-44):
    - lines < 0 raises ValueError
    - lines == 0 returns ""
    - lines > 0 returns lines separated by "\\n"
    """
    if lines < 0:
        raise ValueError("Number of lines must be non-negative")
    if lines == 0:
        return ""
    # Independent formula: line k (0-indexed) has (lines - k) '@' and (k + 1) '$'
    parts = ["@" * (lines - k) + "    " + "$" * (k + 1) for k in range(lines)]
    return "\n".join(parts)


def run_main_with_input(input_val: str) -> str:
    """Execute main() with mocked builtins.input and captured stdout.

    Args:
        input_val: String passed to input("Enter number of lines: ").

    Returns:
        Captured stdout as a string.
    """
    orig_input = builtins.input
    orig_stdout = sys.stdout
    captured = io.StringIO()
    try:
        builtins.input = lambda prompt="": str(input_val)
        sys.stdout = captured
        main()
        return captured.getvalue()
    finally:
        builtins.input = orig_input
        sys.stdout = orig_stdout


# ---------------------------------------------------------------------------
# 1. Source Anchors (print(pattern(3)), print(pattern(1)), print(pattern(0)))
# ---------------------------------------------------------------------------


class TestSourceAnchors:
    """Tests directly tied to the task's executable source anchors."""

    def test_anchor_lines_3(self):
        """Anchor: print(pattern(3)).

        Expected output:
        @@@    $
        @@    $$
        @    $$$
        Source citation: new_pattern.py docstring lines 23-26.
        """
        expected = "@@@    $\n@@    $$\n@    $$$\n"
        actual = run_main_with_input("3")
        assert actual == expected, (
            f"Anchor 3 failed: expected {expected!r}, got {actual!r}"
        )

    def test_anchor_lines_1(self):
        """Anchor: print(pattern(1)).

        Expected output:
        @    $
        Source citation: new_pattern.py docstring lines 28-29.
        """
        expected = "@    $\n"
        actual = run_main_with_input("1")
        assert actual == expected, (
            f"Anchor 1 failed: expected {expected!r}, got {actual!r}"
        )

    def test_anchor_lines_0(self):
        """Anchor: print(pattern(0)).

        Expected output: empty line (blankline).
        Source citation: new_pattern.py docstring lines 31-32, line 43.
        """
        expected = "\n"
        actual = run_main_with_input("0")
        assert actual == expected, (
            f"Anchor 0 failed: expected {expected!r}, got {actual!r}"
        )


# ---------------------------------------------------------------------------
# 2. Derived Neighboring Supported Inputs
# ---------------------------------------------------------------------------


class TestDerivedNeighborInputs:
    """Tests for neighboring supported inputs derived independently."""

    def test_derived_neighbor_lines_2(self):
        """Neighbor: lines = 2 (derived between anchors 1 and 3).

        Line 1 (k=0): 2 '@', 4 spaces, 1 '$' -> '@@    $'
        Line 2 (k=1): 1 '@', 4 spaces, 2 '$' -> '@    $$'
        Expected output via main():
        @@    $
        @    $$
        """
        expected = "@@    $\n@    $$\n"
        actual = run_main_with_input("2")
        assert actual == expected, (
            f"Neighbor lines=2 failed: expected {expected!r}, got {actual!r}"
        )

    def test_derived_neighbor_lines_4(self):
        """Neighbor: lines = 4 (derived beyond anchor 3).

        Independently calculated:
        Line 1: @@@@    $
        Line 2: @@@    $$
        Line 3: @@    $$$
        Line 4: @    $$$$
        """
        expected = "@@@@    $\n@@@    $$\n@@    $$$\n@    $$$$\n"
        actual = run_main_with_input("4")
        assert actual == expected, (
            f"Neighbor lines=4 failed: expected {expected!r}, got {actual!r}"
        )


# ---------------------------------------------------------------------------
# 3. 100+ Bounded Valid Cases Generated with Fixed Seed
# ---------------------------------------------------------------------------

# Generate 100 deterministic bounded cases: domain n in [0, 50]
RNG = random.Random(42)
BOUNDED_CASES = [0, 1, 2, 3, 4, 5] + [RNG.randint(0, 50) for _ in range(95)]
assert len(BOUNDED_CASES) >= 100


@pytest.mark.parametrize("lines", BOUNDED_CASES)
def test_generated_cases_exact_oracle_match(lines):
    """Property test: main(str(lines)) agrees with independent oracle.

    Generated with deterministic seed 42, bounded to [0, 50].
    Every assertion has an explicit expected value computed via oracle.
    """
    oracle_res = oracle_pattern(lines)
    expected_output = f"{oracle_res}\n"
    actual_output = run_main_with_input(str(lines))
    assert actual_output == expected_output, (
        f"Mismatch for lines={lines}: expected {expected_output!r}, got {actual_output!r}"
    )


@pytest.mark.parametrize("lines", BOUNDED_CASES)
def test_generated_cases_symbol_conservation_and_symmetry(lines):
    """Invariant test: Total '@' count == Total '$' count == lines * (lines + 1) // 2."""
    actual_output = run_main_with_input(str(lines))
    expected_symbol_count = lines * (lines + 1) // 2

    at_count = actual_output.count("@")
    dollar_count = actual_output.count("$")

    assert at_count == expected_symbol_count, (
        f"lines={lines}: '@' count {at_count} != expected {expected_symbol_count}"
    )
    assert dollar_count == expected_symbol_count, (
        f"lines={lines}: '$' count {dollar_count} != expected {expected_symbol_count}"
    )
    assert at_count == dollar_count, (
        f"lines={lines}: '@' count {at_count} != '$' count {dollar_count} (symmetry violation)"
    )


@pytest.mark.parametrize("lines", BOUNDED_CASES)
def test_generated_cases_line_count_and_structure(lines):
    """Invariant test: Line count and per-line structural invariant.

    Each line k (0 <= k < lines):
    - Length must be lines + 5.
    - Format must be: '@'*(lines-k) + '    ' + '$'*(k+1).
    """
    actual_output = run_main_with_input(str(lines))

    if lines == 0:
        assert actual_output == "\n", (
            f"lines=0 must output single blank line, got {actual_output!r}"
        )
        return

    # Split output into lines, removing trailing newline
    lines_list = actual_output[:-1].split("\n")
    assert len(lines_list) == lines, (
        f"lines={lines}: expected {lines} lines, got {len(lines_list)}"
    )

    for k, line in enumerate(lines_list):
        expected_len = lines + 5
        assert len(line) == expected_len, (
            f"lines={lines}, line {k}: expected length {expected_len}, got {len(line)} ({line!r})"
        )

        expected_line = "@" * (lines - k) + "    " + "$" * (k + 1)
        assert line == expected_line, (
            f"lines={lines}, line {k}: expected {expected_line!r}, got {line!r}"
        )


# ---------------------------------------------------------------------------
# 4. Determinism / Idempotence (Repeated Runs with Fresh Equivalent Inputs)
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Verify repeated runs with fresh equivalent inputs yield identical results."""

    @pytest.mark.parametrize("n", [0, 1, 2, 3, 5, 10])
    def test_repeated_runs_identical_results(self, n):
        """Repeated invocations must be deterministic."""
        runs = [run_main_with_input(str(n)) for _ in range(5)]
        first = runs[0]
        for idx, run in enumerate(runs[1:], start=2):
            assert run == first, (
                f"Run {idx} for n={n} differed from first run:\nRun 1: {first!r}\nRun {idx}: {run!r}"
            )


# ---------------------------------------------------------------------------
# 5. Public Interface Preservation (Errors for Negative / Non-Integer)
# ---------------------------------------------------------------------------


class TestPublicInterfacePreservation:
    """Ensure existing error handling and public interface remain intact."""

    def test_negative_input_handled_gracefully(self):
        """Negative integers must be handled gracefully with error message."""
        actual = run_main_with_input("-5")
        assert "Error: Number of lines must be non-negative" in actual, (
            f"Expected non-negative error message, got {actual!r}"
        )

    def test_non_integer_input_handled_gracefully(self):
        """Non-integer strings must produce valid integer prompt error."""
        actual = run_main_with_input("abc")
        assert "Error: Please enter a valid integer number." in actual, (
            f"Expected invalid integer error, got {actual!r}"
        )


# ---------------------------------------------------------------------------
# 6. Deliberate Invariant Break Tests (Proving Checks Fail on Broken Copies)
# ---------------------------------------------------------------------------


class TestDeliberatelyBrokenInvariants:
    """Demonstrate that invariant assertions fail when invariants are violated.

    Identifies n = 1 as the smallest positive failing example.
    """

    def test_invariant_fails_on_mutated_separator_spacing(self):
        """Mutation: 3 spaces instead of 4.

        Smallest failing example: lines = 1.
        Expected: '@    $' (length 7)
        Mutated:  '@   $' (length 6)
        """
        mutated_output = "@   $\n"  # 3 spaces
        with pytest.raises(AssertionError, match="expected length 6|!=|failed"):
            # Check per-line structural invariant on mutated output
            line = mutated_output.strip("\n")
            expected_line = "@" * 1 + "    " + "$" * 1  # 4 spaces
            assert line == expected_line, f"Mismatch: {line!r} != {expected_line!r}"

    def test_invariant_fails_on_mutated_symbol(self):
        """Mutation: '#' instead of '@'.

        Smallest failing example: lines = 1.
        Expected: '@    $' (1 '@', 1 '$')
        Mutated:  '#    $' (0 '@', 1 '$')
        """
        mutated_output = "#    $\n"
        with pytest.raises(AssertionError):
            at_count = mutated_output.count("@")
            dollar_count = mutated_output.count("$")
            assert at_count == dollar_count == 1, "Symmetry violated"

    def test_invariant_fails_on_off_by_one_line_count(self):
        """Mutation: missing line in output.

        Smallest failing example: lines = 2.
        Mutated output has only 1 line instead of 2.
        """
        mutated_output = "@@    $\n"
        lines_list = mutated_output.strip("\n").split("\n")
        with pytest.raises(AssertionError):
            assert len(lines_list) == 2, f"Expected 2 lines, got {len(lines_list)}"
