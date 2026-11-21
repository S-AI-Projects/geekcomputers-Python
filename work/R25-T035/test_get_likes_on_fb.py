"""Repeatability and dependency-isolation regression tests for get_likes_on_FB.

Task: R25-T035
Target: get_likes_on_FB.py — get_likes_on_FB (line 1)

Verifies:
1. Smallest valid input with independently calculated expected output (citing source lines).
2. Ordinary input with independently calculated expected output (citing source lines).
3. Repeatability: running the same fixture twice in fresh isolated state produces identical output.
4. Input isolation: running fixture after an intervening call confirms earlier runs cannot alter later results.
5. Deterministic execution: mock opener used; zero live network, user account, or GUI interaction.
6. Public interface: introduced dependency parameters have defaults preserving current callers.
"""

import inspect
import io
import json
import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from get_likes_on_FB import get_likes_on_FB


# ---------------------------------------------------------------------------
# Test Fixtures & Helpers
# ---------------------------------------------------------------------------

SMALLEST_VALID_PAYLOAD = {
    "data": [
        {
            "created_time": "2026-01-01T00:00:00",
        }
    ]
}

ORDINARY_PAYLOAD = {
    "data": [
        {
            "created_time": "2026-11-21T15:30:45",
            "shares": {"count": 25},
            "likes": {"count": 150},
        }
    ]
}

MULTI_ITEM_PAYLOAD = {
    "data": [
        {
            "created_time": "2026-05-10T12:00:00",
            "shares": {"count": 10},
            "likes": {"count": 50},
        },
        {
            "created_time": "2026-08-20T18:45:12",
            "shares": {"count": 5},
            "likes": {"count": 80},
        },
    ]
}


def make_mock_opener(payload_dict, url_collector=None):
    """Create a mock URL opener returning an in-memory JSON stream."""
    def opener(url):
        if url_collector is not None:
            url_collector.append(url)
        raw_bytes = json.dumps(payload_dict).encode("utf-8")
        return io.BytesIO(raw_bytes)
    return opener


def run_with_captured_stdout(func, *args, **kwargs):
    """Execute func while capturing stdout."""
    orig_stdout = sys.stdout
    captured = io.StringIO()
    try:
        sys.stdout = captured
        result = func(*args, **kwargs)
        return result, captured.getvalue()
    finally:
        sys.stdout = orig_stdout


# ---------------------------------------------------------------------------
# 1. Smallest Valid Input & Ordinary Input (Contract & Line Citations)
# ---------------------------------------------------------------------------


class TestGetLikesContractAndFixtures:
    """Tests establishing preconditions and exact output calculations."""

    def test_smallest_valid_input(self):
        """Smallest valid input: single post with created_time, no shares or likes keys.

        Source Precondition Citations:
            - Line 8: userId required string ("4")
            - Line 19: opener returns decodable JSON dict
            - Line 24: data["data"] contains list of 1 post object
            - Lines 25-27: 'created_time' at least 19 chars ->
                time = '00:00:00' [line 25]
                date = '01-01' [line 26]
                year = '2026' [line 27]
            - Lines 29-32: 'shares' not in item -> num_share = 0
            - Lines 33-36: 'likes' not in item -> num_like = 0
            - Line 37: id incremented to 1
            - Line 22: initial print("0")
            - Lines 38-48: tab-separated line: "1\\t00:00:00\\t01-01\\t2026\\t0\\t0"

        Independent expected calculation:
            stdout: "0\\n1\\t00:00:00\\t01-01\\t2026\\t0\\t0\\n"
            record: id=1, time='00:00:00', date='01-01', year='2026', shares=0, likes=0
        """
        user_id = "4"
        opener = make_mock_opener(SMALLEST_VALID_PAYLOAD)

        records, stdout = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener)

        expected_line = "1\t00:00:00\t01-01\t2026\t0\t0"
        expected_stdout = f"0\n{expected_line}\n"

        assert stdout == expected_stdout, (
            f"Smallest input stdout mismatch: expected {expected_stdout!r}, got {stdout!r}"
        )
        assert len(records) == 1
        assert records[0]["id"] == 1
        assert records[0]["time"] == "00:00:00"
        assert records[0]["date"] == "01-01"
        assert records[0]["year"] == "2026"
        assert records[0]["shares"] == 0
        assert records[0]["likes"] == 0
        assert records[0]["formatted"] == expected_line

    def test_ordinary_input(self):
        """Ordinary input: post with explicit shares count and likes count.

        Source Precondition Citations:
            - Line 8: userId required string ("4")
            - Line 24: data["data"] contains 1 post object
            - Lines 25-27: 'created_time' = '2026-11-21T15:30:45' ->
                time = '15:30:45' [line 25]
                date = '11-21' [line 26]
                year = '2026' [line 27]
            - Lines 29-30: 'shares' in item -> num_share = 25
            - Lines 33-34: 'likes' in item -> num_like = 150
            - Line 37: id incremented to 1
            - Line 22: initial print("0")
            - Lines 38-48: tab-separated line: "1\\t15:30:45\\t11-21\\t2026\\t25\\t150"

        Independent expected calculation:
            stdout: "0\\n1\\t15:30:45\\t11-21\\t2026\\t25\\t150\\n"
            record: id=1, time='15:30:45', date='11-21', year='2026', shares=25, likes=150
        """
        user_id = "4"
        opener = make_mock_opener(ORDINARY_PAYLOAD)

        records, stdout = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener)

        expected_line = "1\t15:30:45\t11-21\t2026\t25\t150"
        expected_stdout = f"0\n{expected_line}\n"

        assert stdout == expected_stdout, (
            f"Ordinary input stdout mismatch: expected {expected_stdout!r}, got {stdout!r}"
        )
        assert len(records) == 1
        assert records[0]["id"] == 1
        assert records[0]["time"] == "15:30:45"
        assert records[0]["date"] == "11-21"
        assert records[0]["year"] == "2026"
        assert records[0]["shares"] == 25
        assert records[0]["likes"] == 150
        assert records[0]["formatted"] == expected_line


# ---------------------------------------------------------------------------
# 2. Repeatability in Fresh Isolated State
# ---------------------------------------------------------------------------


class TestRepeatabilityInFreshState:
    """Verify that running the same fixture twice in fresh isolated state gives identical results."""

    def test_repeatability_smallest_valid_input(self):
        """Run smallest valid fixture twice in fresh state; assert results are identical."""
        user_id = "4"

        # Run 1 in fresh state
        opener_1 = make_mock_opener(SMALLEST_VALID_PAYLOAD)
        records_1, stdout_1 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_1)

        # Run 2 in fresh state
        opener_2 = make_mock_opener(SMALLEST_VALID_PAYLOAD)
        records_2, stdout_2 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_2)

        assert stdout_1 == stdout_2, (
            f"Repeatability failed: stdout 1 {stdout_1!r} != stdout 2 {stdout_2!r}"
        )
        assert records_1 == records_2, (
            f"Repeatability failed: records 1 {records_1} != records 2 {records_2}"
        )

    def test_repeatability_ordinary_input(self):
        """Run ordinary fixture twice in fresh state; assert results are identical."""
        user_id = "4"

        opener_1 = make_mock_opener(ORDINARY_PAYLOAD)
        records_1, stdout_1 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_1)

        opener_2 = make_mock_opener(ORDINARY_PAYLOAD)
        records_2, stdout_2 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_2)

        assert stdout_1 == stdout_2
        assert records_1 == records_2


# ---------------------------------------------------------------------------
# 3. Input Isolation (Intervening Call Cannot Alter Later Result)
# ---------------------------------------------------------------------------


class TestInputIsolation:
    """Verify that earlier executions cannot alter later results."""

    def test_input_isolation_after_intervening_call(self):
        """Run Fixture A, then Fixture B (different valid input), then Fixture A again.

        Assert that the intervening call does not leak state, id counter, or data
        into the subsequent execution of Fixture A.
        """
        user_id = "4"

        # Baseline execution: Fixture A (smallest valid input)
        opener_a1 = make_mock_opener(SMALLEST_VALID_PAYLOAD)
        records_a1, stdout_a1 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_a1)

        # Intervening execution: Fixture B (ordinary input with different data)
        opener_b = make_mock_opener(ORDINARY_PAYLOAD)
        records_b, stdout_b = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_b)
        assert records_b != records_a1, "Intervening fixture must differ from baseline"

        # Post-intervening execution: Fixture A again
        opener_a2 = make_mock_opener(SMALLEST_VALID_PAYLOAD)
        records_a2, stdout_a2 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_a2)

        assert stdout_a2 == stdout_a1, (
            f"Input isolation violated: post-intervening stdout {stdout_a2!r} != initial {stdout_a1!r}"
        )
        assert records_a2 == records_a1, (
            f"Input isolation violated: post-intervening records {records_a2} != initial {records_a1}"
        )
        assert records_a2[0]["id"] == 1, "Counter 'id' must reset to 1 on fresh call"

    def test_input_isolation_multi_item_intervening(self):
        """Run single item fixture after a multi-item intervening execution."""
        user_id = "user123"

        opener_single_1 = make_mock_opener(ORDINARY_PAYLOAD)
        rec_1, out_1 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_single_1)

        opener_multi = make_mock_opener(MULTI_ITEM_PAYLOAD)
        rec_multi, out_multi = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_multi)
        assert len(rec_multi) == 2

        opener_single_2 = make_mock_opener(ORDINARY_PAYLOAD)
        rec_2, out_2 = run_with_captured_stdout(get_likes_on_FB, user_id, opener=opener_single_2)

        assert rec_1 == rec_2
        assert out_1 == out_2


# ---------------------------------------------------------------------------
# 4. Deterministic Seam & Dependency Contract Verification
# ---------------------------------------------------------------------------


class TestDependencySeamAndContract:
    """Verify that dependency injection works and parameters preserve caller defaults."""

    def test_url_construction_matches_contract(self):
        """Verify that url constructed passed to opener matches lines 11-18 specification."""
        urls = []
        opener = make_mock_opener(SMALLEST_VALID_PAYLOAD, url_collector=urls)
        get_likes_on_FB("my_user_id", accessToken="CUSTOM_TOKEN", limit=50, opener=opener)

        expected_url = "https://graph.facebook.com/my_user_id/posts?access_token=CUSTOM_TOKEN&limit=50"
        assert urls == [expected_url], f"URL mismatch: expected {expected_url}, got {urls}"

    def test_default_parameters_preserve_callers(self):
        """Verify any introduced parameter has a default preserving current callers."""
        sig = inspect.signature(get_likes_on_FB)
        params = sig.parameters

        # userId is required (first parameter)
        assert "userId" in params
        assert params["userId"].default is inspect.Parameter.empty

        # accessToken has default preserving lines 7
        assert "accessToken" in params
        assert params["accessToken"].default == "TOKENVALUE"

        # limit has default preserving line 9
        assert "limit" in params
        assert params["limit"].default == 100

        # opener has default preserving unmocked callers
        assert "opener" in params
        assert params["opener"].default is None
