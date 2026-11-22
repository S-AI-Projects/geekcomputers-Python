"""Focused regression tests locking down the contract of my_found in translation_of_sizes_of_underwear_RU.py.

Precondition citations:
    - Source Line 3: `my_dict` maps 'XXS' to country base values [42, 36, 8, 38, 24] and sizes to increments.
    - Source Line 14: `answ = my_dict["XXS"][req[1] - 1] + my_dict[req[0]]` for req[0] != 'XXS'.
    - Source Line 16: `answ = my_dict["XXS"][req[1] - 1]` for req[0] == 'XXS'.
    - Source Line 20: `country` dictionary anchoring country keys {1: "Россия", 2: "Германия", 3: "США", 4: "Франция", 5: "Великобритания"}.
    - Source Line 29: `req = []` user input list of format [size_str, country_idx].
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import translation_of_sizes_of_underwear_RU as underwear


class TestMyFoundContract:
    """Contract tests verifying return values and asserting no observable mutations."""

    def test_smallest_valid_input(self):
        """Smallest valid input: size 'XXS' and country index 1 (Россия).

        Preconditions:
            - Line 3: 'XXS' maps to base array [42, 36, 8, 38, 24].
            - Line 16: For 'XXS', answ = my_dict['XXS'][req[1] - 1].
            - Line 20: country 1 is 'Россия'.
            - Line 29: req format is [size, country_idx].
        Literal input:
            req = ['XXS', 1]
        Independently calculated expected output:
            my_dict['XXS'][1 - 1] = 42
        """
        input_data = ["XXS", 1]
        input_copy = list(input_data)

        # Run function
        result = underwear.my_found(input_data)

        # Assert returned value
        assert result == 42, f"Expected 42, got {result}"

        # Assert input was not mutated
        assert input_data == input_copy, f"Observable mutation detected: {input_data} != {input_copy}"

    def test_ordinary_input(self):
        """Ordinary input: size 'M' and country index 3 (США).

        Preconditions:
            - Line 3: 'XXS'[2] = 8, 'M' = 6.
            - Line 14: For size != 'XXS', answ = my_dict['XXS'][req[1] - 1] + my_dict[req[0]].
            - Line 20: country 3 is 'США'.
        Literal input:
            req = ['M', 3]
        Independently calculated expected output:
            8 + 6 = 14
        """
        input_data = ["M", 3]
        input_copy = list(input_data)

        result = underwear.my_found(input_data)

        assert result == 14, f"Expected 14, got {result}"
        assert input_data == input_copy, f"Observable mutation detected: {input_data} != {input_copy}"

    def test_repeated_value_boundary_stability(self):
        """Repeated-value boundary: back-to-back calls with identical input remain deterministic.

        Preconditions:
            - Line 16: Output depends solely on input query without mutable internal accumulator.
        """
        req_a = ["XXS", 1]
        req_b = ["XXS", 1]

        res_a = underwear.my_found(req_a)
        res_b = underwear.my_found(req_b)

        assert res_a == 42
        assert res_b == 42
        assert res_a == res_b

    def test_maximum_domain_boundary(self):
        """Domain upper boundary: size 'XXXL' and country index 5 (Великобритания).

        Preconditions:
            - Line 3: 'XXS'[4] = 24, 'XXXL' = 14.
            - Line 14: answ = 24 + 14 = 38.
            - Line 20: country 5 is 'Великобритания'.
        Literal input:
            req = ['XXXL', 5]
        Independently calculated expected output:
            38
        """
        input_data = ["XXXL", 5]
        result = underwear.my_found(input_data)
        assert result == 38, f"Expected 38, got {result}"
