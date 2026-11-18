"""Reference-comparison regression tests for date-timeserver.py.

Contract & Preconditions:
    - Precondition Source Line 24: `soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
    - Precondition Source Line 25: `soc.bind((socket.gethostname(), 2905))`
    - Precondition Source Line 26: `soc.listen(5)`
    - Precondition Source Line 28: `clientsocket, addr = soc.accept()`
    - Precondition Source Line 31: `currentTime = time.ctime(time.time()) + "\r\n"`
    - Precondition Source Line 32: `clientsocket.send(currentTime.encode("ascii"))`
    - Precondition Source Line 33: `clientsocket.close()`
"""

import datetime
import os
import runpy
import sys
import unittest.mock as mock
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODULE_PATH = os.path.join(REPO_ROOT, "date-timeserver.py")


def independent_oracle(timestamp: float) -> bytes:
    """Independent reference oracle for POSIX asctime formatting.

    Constructs the date-time string using datetime components and formatting,
    without invoking time.ctime().
    """
    dt = datetime.datetime.fromtimestamp(timestamp)
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month]
    day = f"{dt.day:2d}"
    h = f"{dt.hour:02d}"
    m = f"{dt.minute:02d}"
    s = f"{dt.second:02d}"
    y = f"{dt.year:4d}"
    return f"{weekday} {month} {day} {h}:{m}:{s} {y}\r\n".encode("ascii")


def run_server_iteration(timestamp: float):
    """Executes one iteration of date-timeserver.py with mocked network and clock."""
    mock_soc = mock.MagicMock()
    mock_client = mock.MagicMock()
    # Accept returns mock_client once, then raises KeyboardInterrupt to exit while True
    mock_soc.accept.side_effect = [(mock_client, ("127.0.0.1", 54321)), KeyboardInterrupt]

    with mock.patch("socket.socket", return_value=mock_soc), \
         mock.patch("socket.gethostname", return_value="test-host"), \
         mock.patch("time.time", return_value=timestamp):
        try:
            runpy.run_path(MODULE_PATH)
        except KeyboardInterrupt:
            pass

    return mock_soc, mock_client


class TestDateTimeServerReferenceComparison:
    """Test suite comparing date-timeserver against independent oracle."""

    def test_smallest_valid_input_timestamp_zero(self):
        """Smallest valid input: timestamp 0.0 (Unix epoch start).

        Preconditions:
            - Source line 31 formats `time.ctime(time.time()) + "\r\n"`.
            - Source line 32 transmits ASCII bytes.

        Input:
            timestamp = 0.0
        Expected:
            Calculated via independent_oracle(0.0) without calling time.ctime.
        """
        literal_input = 0.0
        expected_output = independent_oracle(literal_input)

        mock_soc, mock_client = run_server_iteration(literal_input)

        assert mock_client.send.call_count == 1
        actual_output = mock_client.send.call_args[0][0]
        assert isinstance(actual_output, bytes)
        assert actual_output == expected_output, (
            f"Expected {expected_output!r}, got {actual_output!r}"
        )

    def test_ordinary_input_timestamp(self):
        """Ordinary input: timestamp 1700000000.0 (Nov 15, 2023).

        Preconditions:
            - Source lines 31-32 format and transmit ASCII bytes.

        Input:
            timestamp = 1700000000.0
        Expected:
            independent_oracle(1700000000.0)
        """
        literal_input = 1700000000.0
        expected_output = independent_oracle(literal_input)

        mock_soc, mock_client = run_server_iteration(literal_input)

        assert mock_client.send.call_count == 1
        actual_output = mock_client.send.call_args[0][0]
        assert actual_output == expected_output

    def test_socket_lifecycle_preconditions(self):
        """Verify preconditions for socket creation, binding, listening, and closing.

        Preconditions:
            - Source line 24: socket.socket(AF_INET, SOCK_STREAM)
            - Source line 25: soc.bind(('test-host', 2905))
            - Source line 26: soc.listen(5)
            - Source line 33: clientsocket.close()
        """
        mock_soc, mock_client = run_server_iteration(1700000000.0)

        mock_soc.bind.assert_called_once_with(("test-host", 2905))
        mock_soc.listen.assert_called_once_with(5)
        mock_client.close.assert_called_once()

    def test_cross_check_25_small_valid_inputs_against_oracle(self):
        """Enumerate 25 distinct valid inputs across the domain and compare against oracle."""
        test_timestamps = [
            100.0, 500.0, 1000.0, 10000.0, 86400.0, 100000.0,
            500000.0, 1000000.0, 10000000.0, 50000000.0,
            100000000.0, 200000000.0, 500000000.0, 800000000.0,
            1000000000.0, 1100000000.0, 1200000000.0, 1300000000.0,
            1400000000.0, 1500000000.0, 1600000000.0, 1650000000.0,
            1700000000.0, 1720000000.0, 1750000000.0,
        ]
        assert len(test_timestamps) == 25

        for ts in test_timestamps:
            expected = independent_oracle(ts)
            _, mock_client = run_server_iteration(ts)
            actual = mock_client.send.call_args[0][0]
            assert actual == expected, (
                f"Mismatch at timestamp {ts}: expected {expected!r}, got {actual!r}"
            )
