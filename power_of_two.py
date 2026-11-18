"""Check whether a number belongs to the power series of two.

Mathematical Invariant:
    A positive integer n >= 1 is a power of 2 if and only if its binary representation
    contains exactly one set bit: popcount(n) == 1, or bin(n).count('1') == 1.
    Equivalently: (n & (n - 1) == 0) <==> n == 2^k for integer k >= 0.
    Multiplying a power of 2 by 2 yields another power of 2: n == 2^k => 2n == 2^(k+1).

Contract & Preconditions:
    - Precondition Source Line 22: `a = int(input("Enter a number"))` expects a string
      convertible to integer from standard input.
    - Precondition Source Line 23: `if a & (a - 1) == 0:` evaluates bitwise invariant.
    - Precondition Source Line 24: Outputs 'It comes in  power series of 2'.
    - Precondition Source Line 26: Outputs 'It does not come in  power series of 2'.
"""

# Simple and efficient python program to check whether a number is series of power of two
# Example:
# Input:
# 8
# Output:
# It comes in  power series of 2
a = int(input("Enter a number"))
if a & (a - 1) == 0:
    print("It comes in  power series of 2")
else:
    print("It does not come in  power series of 2")
