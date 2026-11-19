"""Cross-check tests for get_players() from RandomNumberGame.py.

Task: R25-T033
Target: RandomNumberGame.py — get_players (line 28)

Each test mocks builtins.input, calls get_players, and compares the result
against an independently calculated expected value (the oracle). The oracle
does NOT call get_players; it independently constructs the expected list.

Fixture anchors (from task specification):
    >>> import builtins, random
    >>> random.seed(0)
    >>> inputs = iter(["1", "Alice", "50", "49"])
Plus one neighboring supported input derived independently.
"""

import builtins
import sys
import os
import pytest

# Ensure the repo root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from RandomNumberGame import get_players


# ---------------------------------------------------------------------------
# Independent Oracle
# ---------------------------------------------------------------------------


def oracle_get_players(names_sequence, n):
    """Independent reference implementation for get_players.

    Constructs the expected result without calling get_players.
    Contract (source line 46): return [input(...) for _ in range(n)]
      - Returns a list of exactly n strings from sequential input() calls.
      - Order is preserved (list comprehension over range(n)).

    Args:
        names_sequence: list of strings that input() would return.
        n: number of players.

    Returns:
        list[str]: first n items from names_sequence, in order.
    """
    return list(names_sequence[:n])


# ---------------------------------------------------------------------------
# Helper: mock input and run get_players
# ---------------------------------------------------------------------------


def run_get_players_with_mock(names, n):
    """Mock builtins.input and call get_players(n).

    Returns the actual result from get_players.
    """
    original_input = builtins.input
    names_iter = iter(names)
    builtins.input = lambda prompt="": next(names_iter)
    try:
        return get_players(n)
    finally:
        builtins.input = original_input


# ---------------------------------------------------------------------------
# Test: Task-specified fixture (anchor inputs)
# ---------------------------------------------------------------------------


class TestGetPlayersAnchorFixture:
    """Tests using the task-specified executable source anchors."""

    def test_anchor_fixture_single_player(self):
        """Anchor fixture: n=1, input="Alice".

        Source anchors:
            >>> import builtins, random
            >>> random.seed(0)
            >>> inputs = iter(["1", "Alice", "50", "49"])
        get_players is called with n=1 (the "1" is consumed by play_game
        for player count). The first name input is "Alice".

        Source: Line 46 — list comprehension collects 1 input() call.
        """
        names = ["Alice"]
        n = 1
        expected = oracle_get_players(names, n)  # ["Alice"]
        actual = run_get_players_with_mock(names, n)
        assert actual == expected == ["Alice"], (
            f"Anchor fixture: expected {expected}, got {actual}. "
            "Source: Line 46, range(1) → 1 input() call"
        )

    def test_anchor_fixture_neighboring_input(self):
        """Neighboring supported input derived from anchor: n=2, ["Bob", "Charlie"].

        Derived by changing n from 1 to 2 and providing two distinct names.
        Source: Line 46 — list comprehension collects 2 input() calls.
        """
        names = ["Bob", "Charlie"]
        n = 2
        expected = oracle_get_players(names, n)  # ["Bob", "Charlie"]
        actual = run_get_players_with_mock(names, n)
        assert actual == expected == ["Bob", "Charlie"], (
            f"Neighboring input: expected {expected}, got {actual}. "
            "Source: Line 46, range(2) → 2 input() calls"
        )


# ---------------------------------------------------------------------------
# Test: 20+ small valid inputs enumerated
# ---------------------------------------------------------------------------


# Enumerate 25 test cases: (n, names_list, expected_result)
CROSS_CHECK_CASES = [
    # --- n=0 (boundary: empty list) ---
    (0, [], []),
    # --- n=1 (single player, various names) ---
    (1, ["Alice"], ["Alice"]),
    (1, ["Bob"], ["Bob"]),
    (1, [""], [""]),
    (1, ["X"], ["X"]),
    (1, ["Player 1"], ["Player 1"]),
    # --- n=2 (two players) ---
    (2, ["Alice", "Bob"], ["Alice", "Bob"]),
    (2, ["Zoe", "Amy"], ["Zoe", "Amy"]),
    (2, ["", ""], ["", ""]),
    (2, ["player-one", "player-two"], ["player-one", "player-two"]),
    # --- n=3 (three players) ---
    (3, ["A", "B", "C"], ["A", "B", "C"]),
    (3, ["Alice", "Bob", "Charlie"], ["Alice", "Bob", "Charlie"]),
    (3, ["foo", "bar", "baz"], ["foo", "bar", "baz"]),
    # --- n=4 ---
    (4, ["P1", "P2", "P3", "P4"], ["P1", "P2", "P3", "P4"]),
    # --- n=5 ---
    (5, ["a", "b", "c", "d", "e"], ["a", "b", "c", "d", "e"]),
    # --- Special string values ---
    (1, ["  spaces  "], ["  spaces  "]),
    (1, ["123"], ["123"]),
    (1, ["name_with_underscore"], ["name_with_underscore"]),
    (1, ["CamelCase"], ["CamelCase"]),
    (2, ["UPPER", "lower"], ["UPPER", "lower"]),
    # --- Duplicate names (get_players doesn't deduplicate) ---
    (3, ["Same", "Same", "Same"], ["Same", "Same", "Same"]),
    # --- Unicode names ---
    (1, ["日本語"], ["日本語"]),
    (2, ["Ñoño", "Ürgen"], ["Ñoño", "Ürgen"]),
    # --- Longer lists ---
    (6, ["p1", "p2", "p3", "p4", "p5", "p6"],
     ["p1", "p2", "p3", "p4", "p5", "p6"]),
    (7, ["a", "b", "c", "d", "e", "f", "g"],
     ["a", "b", "c", "d", "e", "f", "g"]),
]


@pytest.mark.parametrize(
    "n, names, expected",
    CROSS_CHECK_CASES,
    ids=[
        "n0_empty",
        "n1_alice", "n1_bob", "n1_empty_string", "n1_single_char",
        "n1_with_space",
        "n2_alice_bob", "n2_zoe_amy", "n2_empty_strings",
        "n2_hyphenated",
        "n3_abc", "n3_alice_bob_charlie", "n3_foo_bar_baz",
        "n4_p1234",
        "n5_abcde",
        "n1_leading_trailing_spaces", "n1_numeric_string",
        "n1_underscore", "n1_camelcase",
        "n2_upper_lower",
        "n3_duplicate_names",
        "n1_unicode_japanese", "n2_unicode_latin",
        "n6_six_players", "n7_seven_players",
    ],
)
def test_get_players_cross_check(n, names, expected):
    """Cross-check get_players against independent oracle.

    For each case:
    1. Oracle independently computes expected = names[:n]
    2. get_players(n) is called with mocked input
    3. Results are compared

    Source: Line 46 — [input(...) for _ in range(n)]
    Contract: returns list of exactly n strings in input order.
    """
    # Independent oracle calculation
    oracle_result = oracle_get_players(names, n)
    assert oracle_result == expected, (
        f"Oracle self-check failed: oracle={oracle_result}, expected={expected}"
    )

    # Actual function under test
    actual = run_get_players_with_mock(names, n)

    # Cross-check: actual must match oracle
    assert actual == oracle_result, (
        f"Cross-check mismatch for n={n}, names={names}: "
        f"get_players returned {actual}, oracle expected {oracle_result}. "
        "Source: Line 46, list comprehension over range(n)"
    )


# ---------------------------------------------------------------------------
# Test: Repeated runs with fresh equivalent inputs give same result
# ---------------------------------------------------------------------------


class TestGetPlayersReproducibility:
    """Verify that repeated runs with fresh equivalent inputs give same result."""

    def test_reproducibility_single_player(self):
        """Repeated calls with same inputs produce identical results.

        Source: Line 46 — deterministic list comprehension (no randomness).
        """
        names = ["Alice"]
        n = 1
        results = [run_get_players_with_mock(names, n) for _ in range(5)]
        assert all(r == ["Alice"] for r in results), (
            f"Non-reproducible results: {results}. "
            "Source: Line 46, deterministic comprehension"
        )

    def test_reproducibility_multiple_players(self):
        """Repeated calls with same multi-player inputs produce identical results.

        Source: Line 46 — deterministic list comprehension.
        """
        names = ["A", "B", "C"]
        n = 3
        results = [run_get_players_with_mock(names, n) for _ in range(5)]
        assert all(r == ["A", "B", "C"] for r in results), (
            f"Non-reproducible results: {results}. "
            "Source: Line 46, deterministic comprehension"
        )

    def test_reproducibility_empty(self):
        """Repeated calls with n=0 always return empty list.

        Source: Line 46 — range(0) produces no iterations.
        """
        results = [run_get_players_with_mock([], 0) for _ in range(5)]
        assert all(r == [] for r in results), (
            f"Non-reproducible results: {results}. "
            "Source: Line 46, range(0) → empty list"
        )


# ---------------------------------------------------------------------------
# Test: Order preservation
# ---------------------------------------------------------------------------


class TestGetPlayersOrdering:
    """Verify that names appear in the exact order input() returns them."""

    def test_order_is_preserved(self):
        """Names must appear in input order, not sorted or shuffled.

        Source: Line 46 — list comprehension iterates range(n) sequentially.
        """
        names = ["Zara", "Alice", "Mike", "Bob"]
        n = 4
        expected = oracle_get_players(names, n)
        actual = run_get_players_with_mock(names, n)
        assert actual == expected == ["Zara", "Alice", "Mike", "Bob"], (
            f"Order not preserved: expected {expected}, got {actual}. "
            "Source: Line 46, sequential iteration"
        )

    def test_reverse_order(self):
        """Reversed input order is preserved as-is.

        Source: Line 46 — no sorting applied.
        """
        names = ["D", "C", "B", "A"]
        n = 4
        expected = oracle_get_players(names, n)
        actual = run_get_players_with_mock(names, n)
        assert actual == expected == ["D", "C", "B", "A"], (
            "Source: Line 46, no reordering"
        )


# ---------------------------------------------------------------------------
# Test: Return type contract
# ---------------------------------------------------------------------------


class TestGetPlayersReturnContract:
    """Verify the documented return/mutation contract."""

    def test_returns_list(self):
        """Return type must be list.

        Source: Line 29 — type hint List[str].
        """
        actual = run_get_players_with_mock(["A"], 1)
        assert isinstance(actual, list), (
            f"Expected list, got {type(actual)}. Source: Line 29 type hint"
        )

    def test_returns_strings(self):
        """All elements must be strings.

        Source: Line 29 — type hint List[str], Line 46 — input() returns str.
        """
        actual = run_get_players_with_mock(["A", "B"], 2)
        assert all(isinstance(x, str) for x in actual), (
            f"Non-string elements in result. Source: Line 29/46"
        )

    def test_length_matches_n(self):
        """Result length must equal n.

        Source: Line 46 — range(n) produces exactly n iterations.
        """
        for n in range(6):
            names = [f"P{i}" for i in range(n)]
            actual = run_get_players_with_mock(names, n)
            assert len(actual) == n, (
                f"Length mismatch: expected {n}, got {len(actual)}. "
                "Source: Line 46, range(n)"
            )

