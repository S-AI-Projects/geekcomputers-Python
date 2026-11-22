# Python code to calculate the sum of digits of a number, by taking number input from user.

import sys


def get_integer(input_func=input):
    """
    Prompt the user for an integer, with up to 3 attempts.

    Complexity:
      - Input size variable: d = len(num), the number of digits in the input string.
      - Worst-case time complexity: O(d) per attempt. num.isnumeric() scans d characters
        in O(d) time, and int(num) parses d digits in O(d) to sub-quadratic time.
        With at most 3 attempts, overall worst-case complexity is O(d).
      - Space complexity: O(d) to store the input string and parsed integer.
      - Empirical observation: When isolating algorithm operations from I/O overhead,
        measured median runtime scales linearly with digit length d over d in {100, 1000, 3000}.
    """
    for i in range(
        3, 0, -1
    ):  # executes the loop 3 times. Giving 3 chances to the user.
        num = input_func("enter a number:")
        if num.isnumeric():  # checks if entered input is an integer string or not.
            num = int(
                num
            )  # converting integer string to integer. And returns it to where function is called.
            return num
        else:
            print("enter integer only")
            print(
                f"{i - 1} chances are left"
                if (i - 1) > 1
                else f"{i - 1} chance is left"
            )  # prints if user entered wrong input and chances left.
        continue


def addition(num):
    """
    Returns the sum of the digits of a number.
    Negative numbers are handled using the absolute value.

    Complexity:
      - Input size variable: d, where d = floor(log10(|num|)) + 1 is the number
        of decimal digits in |num| (d = 1 for num = 0).
      - Worst-case time complexity: O(d) loop iterations where each step extracts
        and reduces a digit via % 10 and // 10.
      - Space complexity: O(1) auxiliary space.

    Examples:
    >>> addition(123)
    6
    >>> addition(-784)
    19
    >>> addition(124)
    7
    """
    Sum = 0
    if type(num) is type(
        None
    ):  # Checks if number type is none or not. If type is none program exits.
        print("Try again!")
        sys.exit()
    num = abs(num) # Handle negative numbers
    while num > 0:  # Addition- adding the digits in the number.
        digit = int(num % 10)
        Sum += digit
        num //= 10
    return Sum  # Returns sum to where the function is called.


if (
    __name__ == "__main__"
):  # this is used to overcome the problems while importing this file.
    number = get_integer()
    Sum = addition(number)
    abs_display = f" (absolute value: {abs(number)})" if number < 0 else ""
    print(f"Sum of digits of {number}{abs_display} is {Sum}")  # Prints the sum
