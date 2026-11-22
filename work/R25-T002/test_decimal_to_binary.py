"""Focused boundary regression tests for decimal_to_binary in Decimal number to binary function.py.

Precondition citations:
    - Source Line 2: `number = int(input(...))` establishes integer coercion contract.
    - Source Line 5: `bin(number)` generates binary representation with '0b' prefix.
"""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Load module dynamically because filename contains spaces
TARGET_PATH = REPO_ROOT / "Decimal number to binary function.py"
spec = importlib.util.spec_from_file_location("dec2bin_mod", str(TARGET_PATH))
dec2bin = importlib.util.module_from_spec(spec)
sys.modules["dec2bin_mod"] = dec2bin
spec.loader.exec_module(dec2bin)


class TestDecimalToBinaryBoundaries:
    """Boundary test suite verifying supported domain boundaries and edge cases."""

    def test_smallest_valid_input_zero(self):
        """Smallest non-negative input: 0.

        Preconditions:
            - Source line 2: int(0) evaluates to 0.
            - Source line 5: bin(0) evaluates to '0b0'.
        Literal input:
            0
        Expected output:
            '0b0'
        """
        assert dec2bin.decimal_to_binary(0) == "0b0"
        assert dec2bin.decimal_number_to_binary_function(0) == "0b0"

    def test_ordinary_input(self):
        """Ordinary positive integer: 10.

        Preconditions:
            - Source line 2: int(10) evaluates to 10.
            - Source line 5: bin(10) evaluates to '0b1010'.
        Literal input:
            10
        Expected output:
            '0b1010'
        """
        assert dec2bin.decimal_to_binary(10) == "0b1010"

    def test_unit_boundary_positive(self):
        """Unit positive boundary: 1.

        Literal input:
            1
        Expected output:
            '0b1'
        """
        assert dec2bin.decimal_to_binary(1) == "0b1"

    def test_negative_unit_boundary(self):
        """Negative unit boundary: -1.

        Preconditions:
            - Source line 2: int(-1) evaluates to -1.
            - Source line 5: bin(-1) evaluates to '-0b1'.
        Literal input:
            -1
        Expected output:
            '-0b1'
        """
        assert dec2bin.decimal_to_binary(-1) == "-0b1"

    def test_negative_ordinary_boundary(self):
        """Ordinary negative integer boundary: -10.

        Literal input:
            -10
        Expected output:
            '-0b1010'
        """
        assert dec2bin.decimal_to_binary(-10) == "-0b1010"

    def test_string_numeric_boundary(self):
        """String input representing integer: '42'.

        Preconditions:
            - Source line 2: int('42') coerces to 42.
            - Source line 5: bin(42) produces '0b101010'.
        Literal input:
            '42'
        Expected output:
            '0b101010'
        """
        assert dec2bin.decimal_to_binary("42") == "0b101010"

    def test_large_integer_boundary(self):
        """Power of two boundary: 1024.

        Literal input:
            1024
        Expected output:
            '0b10000000000'
        """
        assert dec2bin.decimal_to_binary(1024) == "0b10000000000"
