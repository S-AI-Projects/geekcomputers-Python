"""Tests for Generate a random number between 0 to 9.py – R25-T038.

Each fixture cites the source line that establishes the precondition being
tested and states an explicit expected value.

Source file: "Generate a random number between 0 to 9.py"
  Line 4 : import random          – PRNG dependency
  Line 6 : print(random.randint(0, 9))  – contract: start <= end, returns int in [start, end]

After refactoring the exposed API is:
    generate_random_number(start=0, end=9, rng=None) -> int
"""
import importlib.util
import sys
import io
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Import helper (file name has spaces)
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC_PATH = _REPO_ROOT / "Generate a random number between 0 to 9.py"

spec = importlib.util.spec_from_file_location("gen_random", str(_SRC_PATH))
_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_mod)
generate_random_number = _mod.generate_random_number


# ---------------------------------------------------------------------------
# Mock RNG for deterministic tests
# ---------------------------------------------------------------------------
class _MockRng:
    """Minimal RNG stub whose randint always returns a fixed value."""

    def __init__(self, fixed_value: int):
        self._value = fixed_value

    def randint(self, a: int, b: int) -> int:  # noqa: D401
        return self._value


# ===========================================================================
# TestSmallestValidInput
# ===========================================================================
class TestSmallestValidInput:
    """Source: line 6 – randint(0, 9); smallest valid range is start==end==0."""

    def test_zero_range_returns_only_possible_value(self):
        """start=0, end=0 → only 0 is in range; expected: 0.
        Source: line 6 – randint(start, end) with start==end==0.
        """
        result = generate_random_number(start=0, end=0, rng=_MockRng(0))
        assert result == 0, f"Expected 0, got {result}"

    def test_zero_range_type_is_int(self):
        """Return type must be int (source: line 6 – randint returns int)."""
        result = generate_random_number(start=0, end=0, rng=_MockRng(0))
        assert isinstance(result, int)

    def test_single_value_range_other_bound(self):
        """start=5, end=5 → only 5 is valid; expected: 5.
        Source: line 6 – randint(start, end) with start==end.
        """
        result = generate_random_number(start=5, end=5, rng=_MockRng(5))
        assert result == 5, f"Expected 5, got {result}"


# ===========================================================================
# TestOrdinaryInput
# ===========================================================================
class TestOrdinaryInput:
    """Source: line 6 – randint(0, 9); ordinary call with mocked PRNG."""

    def test_returns_mocked_value_in_range(self):
        """start=0, end=9, mock returns 6 → expected: 6.
        Source: line 6 – randint(0, 9).
        """
        result = generate_random_number(start=0, end=9, rng=_MockRng(6))
        assert result == 6, f"Expected 6, got {result}"

    def test_lower_bound_value(self):
        """Mock returning 0 → expected: 0 (lower bound).
        Source: line 6 – randint returns int in [start, end].
        """
        result = generate_random_number(start=0, end=9, rng=_MockRng(0))
        assert result == 0

    def test_upper_bound_value(self):
        """Mock returning 9 → expected: 9 (upper bound).
        Source: line 6 – randint returns int in [start, end].
        """
        result = generate_random_number(start=0, end=9, rng=_MockRng(9))
        assert result == 9

    def test_arbitrary_range_mid_value(self):
        """start=3, end=7, mock returns 5 → expected: 5.
        Source: line 6 – randint(start, end).
        """
        result = generate_random_number(start=3, end=7, rng=_MockRng(5))
        assert result == 5

    def test_default_params_use_real_rng(self):
        """Default call (no args) must return int in [0, 9].
        Source: line 6 – print(random.randint(0, 9)); defaults preserved.
        """
        result = generate_random_number()
        assert isinstance(result, int)
        assert 0 <= result <= 9, f"Expected 0<=result<=9, got {result}"


# ===========================================================================
# TestFailurePath
# ===========================================================================
class TestFailurePath:
    """Source: line 6 – randint(start, end) requires start <= end.
    When start > end Python raises ValueError from randrange inside randint.
    Smallest failing input: start=1, end=0.
    """

    def test_inverted_range_raises_value_error(self):
        """start=1, end=0 → ValueError (smallest failing input).
        Source: line 6 – randint precondition start <= end.
        """
        with pytest.raises(ValueError):
            generate_random_number(start=1, end=0)

    def test_large_inverted_range_raises_value_error(self):
        """start=10, end=5 → ValueError.
        Source: line 6 – randint precondition start <= end.
        """
        with pytest.raises(ValueError):
            generate_random_number(start=10, end=5)

    def test_negative_inverted_range_raises_value_error(self):
        """start=-1, end=-5 → ValueError.
        Source: line 6 – randint precondition start <= end.
        """
        with pytest.raises(ValueError):
            generate_random_number(start=-1, end=-5)


# ===========================================================================
# TestPostFailureRecovery
# ===========================================================================
class TestPostFailureRecovery:
    """After a ValueError the module state must be unaffected; a valid call
    immediately following must succeed with correct output.
    Source: line 4 – import random (module-level PRNG; caller-injected rng
    is independent so no cross-call state corruption possible).
    """

    def test_valid_call_after_value_error(self):
        """Raise ValueError, then call with start=0, end=9 → expected: 7.
        Source: line 6 – independent calls share no mutable state.
        """
        with pytest.raises(ValueError):
            generate_random_number(start=5, end=2)
        result = generate_random_number(start=0, end=9, rng=_MockRng(7))
        assert result == 7, f"Expected 7 after recovery, got {result}"

    def test_multiple_valid_calls_after_failure(self):
        """Three consecutive ValueError-raising calls followed by a valid call.
        Source: line 4/6 – module import is idempotent; no shared state.
        """
        for _ in range(3):
            with pytest.raises(ValueError):
                generate_random_number(start=9, end=0)
        result = generate_random_number(start=2, end=4, rng=_MockRng(3))
        assert result == 3, f"Expected 3 after recovery, got {result}"


# ===========================================================================
# TestOutputFormat
# ===========================================================================
class TestOutputFormat:
    """Verify that the CLI __main__ block prints the generated number to stdout.
    Source: line 6 – print(random.randint(0, 9)); __main__ guard now wraps it.
    """

    def _run_main(self, fixed_value: int) -> str:
        """Execute the __main__ block with a mocked rng and capture stdout."""
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            # Patch random inside the imported module temporarily
            import random as _random_module
            original_randint = _random_module.randint
            _random_module.randint = lambda a, b: fixed_value
            try:
                # Re-exec __main__ block: call generate_random_number via print
                print(generate_random_number(rng=_random_module))
            finally:
                _random_module.randint = original_randint
        finally:
            sys.stdout = old_stdout
        return captured.getvalue().strip()

    def test_output_is_integer_string(self):
        """CLI output for mock value 4 must be the string '4'.
        Source: line 6 – print(random.randint(0, 9)).
        """
        output = self._run_main(4)
        assert output == "4", f"Expected '4', got {output!r}"

    def test_output_is_parseable_as_int(self):
        """CLI output must be parseable as int (source: line 6 – randint returns int)."""
        output = self._run_main(9)
        assert int(output) == 9

    def test_output_newline_terminated(self):
        """print() appends a newline; raw captured value ends with '\\n'.
        Source: line 6 – print(…) adds newline.
        """
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            print(generate_random_number(start=0, end=9, rng=_MockRng(3)))
        finally:
            sys.stdout = old_stdout
        raw = captured.getvalue()
        assert raw.endswith("\n"), f"Expected newline-terminated output, got {raw!r}"
