"""small script to learn how to print out all 4-digit num"""


# ALL the combinations of 4 digit combo
def four_digit_combinations(limit=10000, numbers=None):
    """
    Generate and print zero-padded 4-digit numbers up to limit.

    Contract:
      Preconditions:
        - Line 7: `numbers = []` establishes the default accumulation list fixture.
        - Line 8: `limit` specifies the iteration upper bound (default: 10000, range 0..10000).
        - Line 9: `code = str(code).zfill(4)` pads numeric values into 4-character strings.
        - Line 10: `print(code)` outputs each code to standard output.
        - Line 11: `numbers.append(code)` mutates the accumulation list in-place.
      Postconditions:
        - Returns: List of 4-character strings formatted from range(limit).
        - Side effects / Observable mutation: Outputs to stdout and mutates `numbers` list if passed.
    """
    if numbers is None:
        numbers = []
    for code in range(limit):
        code = str(code).zfill(4)
        print(code)
        numbers.append(code)
    return numbers


# Same as above but more pythonic
def one_line_combinations():
    """print out all 4-digit numbers"""
    numbers = [str(i).zfill(4) for i in range(10000)]
    print(numbers)
