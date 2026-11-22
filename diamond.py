def draw_diamond(n, output_fn=print):
    """
    Draw an ASCII diamond of width and height n where n is an odd integer.

    Contract:
      Preconditions:
        - Line 1: `n` is an integer; `output_fn` defaults to built-in `print`.
        - Line 2: `if n % 2 != 0:` checks if `n` is odd.
        - Line 4: `while k <= n:` upper pyramid expands by 2 until width `n`.
        - Line 5: `print(" " * int((n - k) / 2) + "*" * k + " " * int((n - k) / 2))`
        - Line 9: `while (n - 2 * j) >= 1:` lower inverted pyramid contracts.
        - Line 10: `print(" " * j + "*" * (n - 2 * j) + " " * (j))`
        - Line 14: `else:` outputs rejection message for even integers.
      Determinism:
        - Pure calculation with zero hidden mutable global state.
        - Injectable `output_fn` seam allows deterministic testing without stdout coupling.
    """
    if n % 2 != 0:
        k = 1
        while k <= n:
            output_fn(" " * int((n - k) / 2) + "*" * k + " " * int((n - k) / 2))
            k += 2

        j = 1
        while (n - 2 * j) >= 1:
            output_fn(" " * j + "*" * (n - 2 * j) + " " * (j))
            j += 1
    else:
        output_fn("Not an odd number. Can't draw a diamond :(")


def main():
    n = int(input("Enter an odd number: "))
    draw_diamond(n)


if __name__ == "__main__":
    main()
