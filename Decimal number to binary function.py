# decimal number
def decimal_to_binary(number):
    """Converts a decimal integer to its equivalent binary string representation.

    Contract:
        Preconditions:
            - Source line 2: Input is convertible to an integer via int(number).
            - Source line 5: Formats integer to binary string using built-in bin(number).
        Inputs:
            number (int, float, or numeric str): The decimal number to convert.
        Returns:
            str: Binary representation prefixed with '0b' (or '-0b' for negative values).
        Supported Boundaries:
            - Zero boundary (smallest non-negative input): 0 -> '0b0'
            - Unit boundary: 1 -> '0b1'
            - Ordinary positive: 10 -> '0b1010'
            - Negative unit boundary: -1 -> '-0b1'
            - Large integer boundary: 1024 -> '0b10000000000'
    """
    return bin(int(number))


# Aliases for exact naming match
decimal_number_to_binary_function = decimal_to_binary


def main():
    number = int(input("Enter any decimal number: "))
    # print equivalent binary number
    print("Equivalent Binary Number: ", decimal_to_binary(number))


if __name__ == "__main__":
    main()
