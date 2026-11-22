"""GCD (Greatest Common Divisor) Calculation.

This module provides functions to calculate the greatest common divisor
of two integers using linear search.
"""


def is_common_divisor(i, a, b):
    """Check if integer i divides both a and b evenly without remainder.

    Preconditions & Contract (derived from source line 12):
        - Source line 12: `a % i == 0 and b % i == 0`
        - i must be non-zero to avoid ZeroDivisionError.
        - Returns True if i is a common divisor of both a and b, False otherwise.
    """
    return a % i == 0 and b % i == 0


def gcd(a, b):
    """Compute the greatest common divisor of two integers a and b.

    Preconditions & Contract (by source line citations):
        - Line 6, 7: a and b must be integers.
        - Line 9: candidate divisor i starts at 1.
        - Line 10: initial gcd value is -1 (sentinel for no positive common divisor).
        - Line 11: iterates while i <= a and i <= b.
        - Line 12: checks if i divides both a and b using is_common_divisor.
        - Line 13: updates running gcd with candidate i.
        - Line 14: increments candidate i by 1.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: The greatest common divisor, or -1 if no positive divisor was found.
    """
    i = 1
    result = -1
    while i <= a and i <= b:
        if is_common_divisor(i, a, b):
            result = i
        i = i + 1
    return result


if __name__ == "__main__":
    a = int(input("Enter number 1 (a): "))
    b = int(input("Enter number 2 (b): "))
    gcd_val = gcd(a, b)
    print("\nGCD of {0} and {1} = {2}".format(a, b, gcd_val))
