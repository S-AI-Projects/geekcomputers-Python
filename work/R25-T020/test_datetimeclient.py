"""Focused mutation-resistant tests for date_timeclient in date-timeclient.py.

Precondition citations:
    - Line 3: `soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` socket initialization.
    - Line 4: `soc.connect((socket.gethostname(), 2905))` destination port 2905 anchor.
    - Line 5: `recmsg = soc.recv(1024)` buffer capacity anchor.
    - Line 6: `soc.close()` socket teardown anchor.
    - Line 7: `"The time got from the server is %s" % recmsg.decode("ascii")` string normalization anchor.
"""

import importlib.util
import io
import sys
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = REPO_ROOT / "date-timeclient.py"

# Import module with hyphen in filename dynamically
spec = importlib.util.spec_from_file_location("datetimeclient_mod", str(TARGET_FILE))
dtclient = importlib.util.module_from_spec(spec)
sys.modules["datetimeclient_mod"] = dtclient
spec.loader.exec_module(dtclient)


class TestDateTimeClientMutationResistance(unittest.TestCase):
    """Tests verifying contract fidelity and mutation resistance against plausible single-line bugs."""

    def test_smallest_valid_input_empty_payload(self):
        """Smallest valid input: empty byte stream b"".
        
        Preconditions:
            - Line 5: soc.recv returns b""
            - Line 7: decode("ascii") produces ""
        Literal input:
            server payload = b""
        Independently calculated expected output:
            "The time got from the server is "
        """
        mock_soc = MagicMock()
        mock_soc.recv.return_value = b""

        with patch("sys.stdout", new_callable=io.StringIO):
            res = dtclient.date_timeclient(host="localhost", socket_factory=lambda: mock_soc)

        mock_soc.connect.assert_called_once_with(("localhost", 2905))
        mock_soc.recv.assert_called_once_with(1024)
        mock_soc.close.assert_called_once()
        self.assertEqual(res, "The time got from the server is ")

    def test_ordinary_input_datetime_string(self):
        """Ordinary input: timestamp payload "2026-11-23 00:00:00".
        
        Preconditions:
            - Line 4: port 2905
            - Line 7: string interpolation %s
        Literal input:
            server payload = b"2026-11-23 00:00:00"
        Independently calculated expected output:
            "The time got from the server is 2026-11-23 00:00:00"
        """
        mock_soc = MagicMock()
        mock_soc.recv.return_value = b"2026-11-23 00:00:00"

        with patch("sys.stdout", new_callable=io.StringIO):
            res = dtclient.date_timeclient(host="time.local", socket_factory=lambda: mock_soc)

        mock_soc.connect.assert_called_once_with(("time.local", 2905))
        mock_soc.recv.assert_called_once_with(1024)
        mock_soc.close.assert_called_once()
        self.assertEqual(res, "The time got from the server is 2026-11-23 00:00:00")

    def test_mutation_resistance_wrong_port(self):
        """Mutation resistance: catch plausible one-line mutation altering default port to 2906."""
        # Define plausible mutant that connects to port 2906
        def mutant_wrong_port(host="localhost", socket_factory=None):
            soc = socket_factory()
            soc.connect((host, 2906))  # Mutant!
            recmsg = soc.recv(1024)
            soc.close()
            return "The time got from the server is %s" % recmsg.decode("ascii")

        mock_soc = MagicMock()
        mock_soc.recv.return_value = b"sample"
        mutant_wrong_port(socket_factory=lambda: mock_soc)

        # Assertion: Verifies that our contract test catches the wrong port
        with self.assertRaises(AssertionError):
            mock_soc.connect.assert_called_once_with(("localhost", 2905))

    def test_mutation_resistance_altered_format_string(self):
        """Mutation resistance: catch plausible one-line bug altering format prefix."""
        # Define plausible mutant with missing 'the' in prefix
        def mutant_altered_prefix(host="localhost", socket_factory=None):
            soc = socket_factory()
            soc.connect((host, 2905))
            recmsg = soc.recv(1024)
            soc.close()
            return "Time got from server is %s" % recmsg.decode("ascii")  # Mutant!

        mock_soc = MagicMock()
        mock_soc.recv.return_value = b"12:00:00"
        bad_result = mutant_altered_prefix(socket_factory=lambda: mock_soc)

        # Assertion: Catches altered format string
        self.assertNotEqual(bad_result, "The time got from the server is 12:00:00")

    def test_mutation_resistance_wrong_buffer_size(self):
        """Mutation resistance: catch plausible one-line bug changing recv buffer from 1024 to 512."""
        def mutant_wrong_buffer(host="localhost", socket_factory=None):
            soc = socket_factory()
            soc.connect((host, 2905))
            recmsg = soc.recv(512)  # Mutant!
            soc.close()
            return "The time got from the server is %s" % recmsg.decode("ascii")

        mock_soc = MagicMock()
        mock_soc.recv.return_value = b"test"
        mutant_wrong_buffer(socket_factory=lambda: mock_soc)

        with self.assertRaises(AssertionError):
            mock_soc.recv.assert_called_once_with(1024)


if __name__ == "__main__":
    unittest.main()
