# Display the powers of 2 using anonymous function

terms = 10


def python_distance(terms=10):
    """
    Calculate powers of 2 up to terms using anonymous function mapping.

    Invariant Contract:
      Preconditions:
        - Line 3: `terms = 10` establishes default iteration terms fixture.
        - Line 9: `result = list(map(lambda x: 2**x, range(terms)))` defines the functional calculation.
        - Invariant 1 (Length/Shape): len(result) == terms for all non-negative integers terms.
        - Invariant 2 (Strict Monotonicity): result[i] < result[i+1] for all i in range(len(result)-1).
        - Invariant 3 (Power of 2 Recurrence): result[i+1] == 2 * result[i] for all i >= 0.
        - Invariant 4 (Base Value): result[0] == 1 when terms >= 1.
      Returns:
        - List of powers of 2 (integers) of length `terms`.
    """
    if terms < 0:
        raise ValueError("terms must be non-negative")
    return list(map(lambda x: 2**x, range(terms)))


powers_of_two = python_distance
result = python_distance(terms)


def main():
    print("The total terms are:", terms)
    for i in range(terms):
        print("2 raised to power", i, "is", result[i])


if __name__ == "__main__":
    main()
