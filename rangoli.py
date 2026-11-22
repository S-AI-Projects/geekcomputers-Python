"""Rangoli Model"""


# Prints a rangoli of size n
def print_rangoli(n):
    """
    Print an alphabet rangoli of size n.

    Preconditions:
      - Line 5: `n` is a positive integer (size of the rangoli).
      - Line 7: `width = 4 * n - 3` calculates total line width.
      - Line 14: Decreasing alphabet characters `chr(96 + n - j)` separated by `-`.
      - Line 19: Increasing alphabet characters `chr(97 + n - k)` separated by `-`.
      - Line 24, 38: `string.center(width, "-")` centers and pads line with hyphens.

    Decisive State Transition:
      In rows `i < n`, the uncentered core string retains a trailing hyphen (e.g. `'c-'` at i=1,
      `'c-b-c-'` at i=2). At the center row `i = n`, the final character brings `len(string) == width`
      (9), causing `len(string) < width` (Line 15/21) to evaluate to False, cleanly terminating the
      sequence without an extraneous hyphen (`'c-b-a-b-c'`). When centering uncentered rows with odd
      remaining margins, Python's `str.center` places `(margin // 2) + 1` dashes on the left and
      `margin // 2` on the right, perfectly absorbing the trailing hyphen to yield exact bilateral symmetry.

    Worked Example:
      >>> print_rangoli(3)
      ----c----
      --c-b-c--
      c-b-a-b-c
      --c-b-c--
      ----c----

      Smallest Valid Input (n=1):
      >>> print_rangoli(1)
      a
    """
    # Width of the rangoli
    width = 4 * n - 3

    # String to be printed
    string = ""

    # Loop to print the rangoli
    for i in range(1, n + 1):
        for j in range(0, i):
            string += chr(96 + n - j)
            if len(string) < width:
                string += "-"

        for k in range(i - 1, 0, -1):
            string += chr(97 + n - k)
            if len(string) < width:
                string += "-"

        print(string.center(width, "-"))
        string = ""

    for i in range(n - 1, 0, -1):
        for j in range(0, i):
            string += chr(96 + n - j)
            if len(string) < width:
                string += "-"

        for k in range(i - 1, 0, -1):
            string += chr(97 + n - k)
            if len(string) < width:
                string += "-"

        print(string.center(width, "-"))
        string = ""


if __name__ == "__main__":
    n = int(input())
    print_rangoli(n)
