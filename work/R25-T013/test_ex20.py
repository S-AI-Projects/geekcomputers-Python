"""Focused independent reference comparison tests for print_all in ex20.py.

Precondition citations:
    - Line 6: `def print_all(f):` establishes input interface as readable file/stream.
    - Line 7: `print(f.read())` reads remaining content to EOF and outputs with newline.
    - Line 10: `f.seek(0)` establishes position awareness of the stream.
"""

import io
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import ex20


def independent_reference_oracle(stream):
    """
    Independent reference oracle for stream printing.
    Uses chunk-based readline accumulation without calling stream.read().
    Emulates Python's print(..., end='\\n').
    """
    chunks = []
    while True:
        line = stream.readline()
        if not line:
            break
        chunks.append(line)
    return "".join(chunks) + "\n"


class TestEx20PrintAllReference(unittest.TestCase):
    """Tests comparing print_all against the independent reference oracle across 20+ inputs."""

    SAMPLE_DATASET = [
        "",  # 1: smallest valid input (empty stream)
        "a",  # 2: single character
        "\n",  # 3: newline only
        "hello",  # 4: single word without trailing newline
        "hello\n",  # 5: single line with trailing newline
        "1\n2\n3\n",  # 6: multiple numeric lines
        "   \t  ",  # 7: whitespace and tabs
        "# Python comment\ndef foo(): pass\n",  # 8: code snippet
        "αβγδε",  # 9: unicode text
        "multi\nline\nwith\nempty\n\nlines\n",  # 10: mixed empty lines
        "symbols: !@#$%^&*()_+=-`~[]{}|;':\",./<>?",  # 11: punctuation
        "long: " + ("x" * 300),  # 12: long text
        "trailing spaces    \n",  # 13: trailing spaces
        "windows\r\nnewlines\r\n",  # 14: CRLF endings
        "0000",  # 15: digits
        "mixed 123 abc 456\n",  # 16: alphanumeric
        "quotes 'single' and \"double\"",  # 17: quotes
        "backslash \\ and forward /",  # 18: slashes
        "{\"key\": \"value\", \"count\": 42}",  # 19: json string
        "# Title\n- Item 1\n- Item 2\n",  # 20: markdown list
        "Final test item 21\nwith multiple\nlines.\n",  # 21: multiline ordinary
    ]

    def test_smallest_valid_input(self):
        """Smallest valid input: empty file stream.
        
        Preconditions:
            - Line 6: f is readable
            - Line 7: print(f.read()) on empty string prints empty string + newline = '\n'
        Literal input:
            stream with content ""
        Independently calculated expected output:
            stdout: "\n", stream.tell() == 0
        """
        stream = io.StringIO("")
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            ex20.print_all(stream)
            self.assertEqual(mock_out.getvalue(), "\n")
            self.assertEqual(stream.tell(), 0)

    def test_ordinary_input(self):
        """Ordinary input: multi-line file content.
        
        Preconditions:
            - Line 6: f is readable
            - Line 7: print(f.read())
        Literal input:
            stream with "First line\nSecond line\n"
        Independently calculated expected output:
            stdout: "First line\nSecond line\n\n"
        """
        content = "First line\nSecond line\n"
        stream = io.StringIO(content)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            ex20.print_all(stream)
            self.assertEqual(mock_out.getvalue(), content + "\n")
            self.assertEqual(stream.tell(), len(content))

    def test_stream_mutation_advances_to_eof(self):
        """Test stream position mutation: print_all moves file pointer from 0 to EOF."""
        content = "Testing stream mutation and pointer traversal."
        stream = io.StringIO(content)
        self.assertEqual(stream.tell(), 0)
        with patch("sys.stdout", new_callable=io.StringIO):
            ex20.print_all(stream)
            self.assertEqual(stream.tell(), len(content))

    def test_all_21_inputs_against_independent_oracle(self):
        """Compare print_all output against independent reference oracle across 21 test inputs."""
        for idx, text in enumerate(self.SAMPLE_DATASET):
            with self.subTest(case=idx, text_preview=text[:20]):
                stream_for_target = io.StringIO(text)
                stream_for_oracle = io.StringIO(text)

                # Run oracle
                expected_output = independent_reference_oracle(stream_for_oracle)

                # Run target
                with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
                    ex20.print_all(stream_for_target)
                    actual_output = mock_out.getvalue()

                self.assertEqual(
                    actual_output,
                    expected_output,
                    f"Mismatch on case {idx}: {text!r}"
                )
                self.assertEqual(stream_for_target.tell(), len(text))


if __name__ == "__main__":
    unittest.main()
