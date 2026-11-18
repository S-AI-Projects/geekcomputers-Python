"""
The Luhn Algorithm is widely used for error-checking in various applications, such as verifying credit card numbers.

By building this project, you'll gain experience working with numerical computations and string manipulation.

"""

# TODO: To make it much more better and succint


def verify_card_number(card_number):
    """Validate a card number using the Luhn checksum algorithm.

    Contract & Determinism:
        Preconditions:
            - Source line 25: `card_number[::-1]` requires sequence/string.
            - Source line 29: `int(digit)` requires numeric characters in string.
            - Source line 39: `return total % 10 == 0` returns boolean.
        Purity:
            - Pure function: zero external dependencies, no I/O, no network,
              no clock, no global mutation, and no mutable default arguments.
            - Deterministic: repeated executions with identical inputs produce identical outputs.
            - Input Isolation: subsequent calls are completely independent of prior calls.
        Inputs:
            card_number (str): A string of numeric digits.
        Returns:
            bool: True if card number satisfies Luhn check, False otherwise.
    """
    sum_of_odd_digits = 0
    card_number_reversed = card_number[::-1]
    odd_digits = card_number_reversed[::2]

    for digit in odd_digits:
        sum_of_odd_digits += int(digit)

    sum_of_even_digits = 0
    even_digits = card_number_reversed[1::2]
    for digit in even_digits:
        number = int(digit) * 2
        if number >= 10:
            number = (number // 10) + (number % 10)
        sum_of_even_digits += number
    total = sum_of_odd_digits + sum_of_even_digits
    return total % 10 == 0


def main():
    card_number = "4111-1111-4555-1142"
    card_translation = str.maketrans({"-": "", " ": ""})
    translated_card_number = card_number.translate(card_translation)

    if verify_card_number(translated_card_number):
        print("VALID!")
    else:
        print("INVALID!")


if __name__ == "__main__":
    main()
