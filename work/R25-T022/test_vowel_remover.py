"""Focused boundary regression tests for vowel_remover in 'vowel remover function.py'.

Contract & Preconditions:
    - Precondition Source Line 27: `for l in text:` establishes that `text` must be iterable.
    - Precondition Source Line 28: `l.lower() not in "aeiou"` establishes that `l` has `.lower()`.
    - Precondition Source Line 29: `string += l` establishes that `l` can concatenate to a `str`.
"""

import importlib.util
import os
import sys
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Dynamically import file with spaces in name using importlib
MODULE_PATH = os.path.join(REPO_ROOT, "vowel remover function.py")
spec = importlib.util.spec_from_file_location("vowel_remover_mod", MODULE_PATH)
vowel_remover_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vowel_remover_mod)
vowel_remover = vowel_remover_mod.vowel_remover


class TestVowelRemoverBoundaries:
    """Boundary test suite for vowel_remover."""

    def test_smallest_valid_input_empty_string(self):
        """Smallest valid input: empty string.

        Preconditions:
            - Source line 27: `for l in text:` executes 0 loop iterations for empty string.
            - Source line 31: Returns initial accumulator `string = ""` (line 26).

        Input:
            text = ""
        Expected:
            ""
        """
        literal_input = ""
        expected_output = ""
        actual_output = vowel_remover(literal_input)
        assert actual_output == expected_output, (
            f"Expected {expected_output!r}, got {actual_output!r}"
        )

    def test_ordinary_input(self):
        """Ordinary input containing mixed vowels and consonants.

        Preconditions:
            - Source lines 27-29 filter out 'e', 'o' while preserving 'h', 'l', ' ', 'w', 'r', 'd', '!'.

        Input:
            text = "hello world!"
        Expected:
            "hll wrld!"
        """
        literal_input = "hello world!"
        expected_output = "hll wrld!"
        actual_output = vowel_remover(literal_input)
        assert actual_output == expected_output

    def test_boundary_all_vowels_lowercase_and_uppercase(self):
        """Boundary: input consisting entirely of vowels.

        Preconditions:
            - Source line 28 checks `l.lower() not in "aeiou"`. Every character matches and is skipped.

        Input:
            text = "aeiouAEIOU"
        Expected:
            ""
        """
        literal_input = "aeiouAEIOU"
        expected_output = ""
        actual_output = vowel_remover(literal_input)
        assert actual_output == expected_output

    def test_boundary_no_vowels(self):
        """Boundary: input with zero vowels.

        Preconditions:
            - Source line 28 evaluates true for every character; none are filtered.

        Input:
            text = "rhythm fly pry"
        Expected:
            "rhythm fly pry"
        """
        literal_input = "rhythm fly pry"
        expected_output = "rhythm fly pry"
        actual_output = vowel_remover(literal_input)
        assert actual_output == expected_output

    def test_boundary_single_character_consonant_and_vowel(self):
        """Boundary: single-character inputs at domain limit.

        Preconditions:
            - Source line 27 runs for exactly 1 iteration.
        """
        # Single consonant
        assert vowel_remover("b") == "b"
        assert vowel_remover("Z") == "Z"
        # Single vowel
        assert vowel_remover("a") == ""
        assert vowel_remover("O") == ""

    def test_boundary_non_alphabetic_characters(self):
        """Boundary: whitespace, digits, and punctuation only.

        Preconditions:
            - Source line 28: digits and symbols don't match "aeiou", so they are retained.

        Input:
            text = " 12345!@#$%^ "
        Expected:
            " 12345!@#$%^ "
        """
        literal_input = " 12345!@#$%^ "
        expected_output = " 12345!@#$%^ "
        actual_output = vowel_remover(literal_input)
        assert actual_output == expected_output

    def test_unsupported_non_iterable_raises_typeerror(self):
        """Unsupported domain: non-iterable integer raises TypeError at source line 27."""
        with pytest.raises(TypeError):
            vowel_remover(12345)

    def test_unsupported_non_string_elements_raises_attributeerror(self):
        """Unsupported domain: list of integers raises AttributeError at line 28 (.lower missing)."""
        with pytest.raises(AttributeError):
            vowel_remover([1, 2, 3])
