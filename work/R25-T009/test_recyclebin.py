"""Focused tests and scaling measurements for sid2user in recyclebin.py.

Precondition citations:
    - Source Line 20: `def sid2user(sid):` accepts SID string
    - Source Line 21: `OpenKey(HKEY_LOCAL_MACHINE, ...)` registry key lookup
    - Source Line 25: `QueryValueEx(key, "ProfileImagePath")` value retrieval
    - Source Line 26: `user = value.split("\\")[-1]` extracting username from path
    - Source Line 28: `except Exception: return sid` fallback return
    - Source Line 32: `dirs = ["c:\\Recycler\\", "C:\\Recycled\\", "C:\\$RECYCLE.BIN\\"]` anchor
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import recyclebin


class MockRegistry:
    """Mock registry maintaining SID-to-ProfileImagePath mappings and tracking operations."""

    def __init__(self, mappings=None):
        self.mappings = mappings or {}
        self.open_key_calls = 0
        self.query_value_calls = 0

    def open_key(self, hkey, subkey):
        self.open_key_calls += 1
        sid = subkey.split("\\")[-1]
        if sid in self.mappings:
            return sid  # return handle represented by sid
        raise FileNotFoundError(f"Key not found: {subkey}")

    def query_value(self, key_handle, value_name):
        self.query_value_calls += 1
        if value_name == "ProfileImagePath" and key_handle in self.mappings:
            return (self.mappings[key_handle], 1)
        raise FileNotFoundError(f"Value not found: {value_name}")


class TestSid2UserWorkAndScaling:
    """Tests functional correctness and measures work scaling across input sizes."""

    def test_smallest_valid_input_nobody(self):
        """Smallest valid input: 'S-1-0-0' (Nobody).

        Preconditions:
            - Line 20: sid = 'S-1-0-0'
            - Line 25: ProfileImagePath = r'C:\\Users\\Nobody'
            - Line 26: splits on '\\' and selects 'Nobody'
        Literal input:
            'S-1-0-0'
        Independently calculated expected output:
            'Nobody'
        """
        reg = MockRegistry({"S-1-0-0": r"C:\Users\Nobody"})
        res = recyclebin.sid2user("S-1-0-0", key_opener=reg.open_key, value_querier=reg.query_value)

        assert res == "Nobody", f"Expected 'Nobody', got {res}"
        assert reg.open_key_calls == 1
        assert reg.query_value_calls == 1

    def test_ordinary_input_admin(self):
        """Ordinary input: Domain administrator SID.

        Preconditions:
            - Line 20: sid = 'S-1-5-21-1004336348-1177238915-682003330-512'
            - Line 25: ProfileImagePath = r'C:\\Users\\Administrator'
        Literal input:
            'S-1-5-21-1004336348-1177238915-682003330-512'
        Independently calculated expected output:
            'Administrator'
        """
        sid = "S-1-5-21-1004336348-1177238915-682003330-512"
        reg = MockRegistry({sid: r"C:\Users\Administrator"})
        res = recyclebin.sid2user(sid, key_opener=reg.open_key, value_querier=reg.query_value)

        assert res == "Administrator"

    def test_unregistered_sid_fallback(self):
        """Precondition line 28 fallback: unmapped SID returns literal input string."""
        reg = MockRegistry({})
        res = recyclebin.sid2user("S-1-5-UNKNOWN", key_opener=reg.open_key, value_querier=reg.query_value)
        assert res == "S-1-5-UNKNOWN"

    def test_algorithmic_work_scaling(self):
        """Measures scaling on inputs where path length n scales by orders of magnitude.

        Input size variable: n = length of ProfileImagePath string.
        Verifies:
            - Exactly 1 registry open and 1 value query executed per call O(1).
            - Output username is correctly parsed for all n in {20, 200, 2000, 20000}.
            - No assertion relies on fragile wall-clock timers.
        """
        for depth in [2, 20, 200, 2000]:
            username = f"user_{depth}"
            # Construct nested path: C:\dir\dir\...\<username>
            path = "C:\\" + "\\".join(["subdir"] * depth) + "\\" + username
            sid = f"S-1-SCALE-{depth}"
            reg = MockRegistry({sid: path})

            actual = recyclebin.sid2user(sid, key_opener=reg.open_key, value_querier=reg.query_value)

            # Correctness check at each scale
            assert actual == username
            assert reg.open_key_calls == 1
            assert reg.query_value_calls == 1
