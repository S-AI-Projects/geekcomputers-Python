def main():
    """Main function that gets user input and calls the pattern generation function.

    Contract & Invariants:
    - Input: Prompts via builtins.input for a non-negative integer string.
    - Output: Prints the generated pattern to stdout followed by a newline.
    - Determinism: Given identical input, repeated executions yield identical output.
    - Invariants for valid input lines = n (n >= 0):
      * Line count: For n == 0, prints an empty line; for n > 0, outputs exactly n lines.
      * Character symmetry: count('@') == count('$') == n * (n + 1) // 2.
      * Per-line structure: Line k (0 <= k < n) has (n - k) '@' characters,
        exactly 4 spaces, and (k + 1) '$' characters (total length: n + 5).
    - Smallest testable cases:
      * n = 0: smallest valid boundary (empty pattern).
      * n = 1: smallest positive pattern ('@    $'), smallest failing example if mutated.
    """
    try:
        lines = int(input("Enter number of lines: "))
        if lines < 0:
            raise ValueError("Number of lines must be non-negative")
        result = pattern(lines)
        print(result)
    except ValueError as e:
        if "invalid literal" in str(e):
            print(f"Error: Please enter a valid integer number. {e}")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def pattern(lines: int) -> str:
    """
    Generate a pattern of '@' and '$' characters.

    Args:
        lines: Number of lines to generate in the pattern

    Returns:
        A multiline string containing the specified pattern

    Raises:
        ValueError: If lines is negative

    Invariants for lines = n (n >= 0):
        - Output consists of n newline-separated lines (empty string if n == 0).
        - Symmetric character counts: count('@') == count('$') == n * (n + 1) // 2.
        - Per-line invariant: line k (0 <= k < n) matches format '@'*(n-k) + '    ' + '$'*(k+1).

    Examples:
    >>> print(pattern(3))
    @@@    $
    @@    $$
    @    $$$

    >>> print(pattern(1))
    @    $

    >>> print(pattern(0))
    <BLANKLINE>

    >>> pattern(-5)
    Traceback (most recent call last):
    ...
    ValueError: Number of lines must be non-negative
    """
    if lines < 0:
        raise ValueError("Number of lines must be non-negative")
    if lines == 0:
        return ""

    pattern_lines = []
    for i in range(lines, 0, -1):
        at_pattern = "@" * i
        dollar_pattern = "$" * (lines - i + 1)
        pattern_lines.append(f"{at_pattern}    {dollar_pattern}")

    return "\n".join(pattern_lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    main()
