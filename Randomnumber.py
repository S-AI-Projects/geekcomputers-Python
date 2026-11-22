# Program to generate a random number between 0 and 9

# importing the random module
from random import randint


def random_number(start=0, end=9):
    """Generates a pseudo-random integer between start and end (inclusive).

    Contract:
        Preconditions:
            - Source line 4: Uses `randint` imported from `random`.
            - Source line 6: Pre-configured domain is [0, 9] inclusive.
        Inputs:
            start (int): Lower bound of the interval (default 0).
            end (int): Upper bound of the interval (default 9).
        Returns:
            int: Random integer satisfying start <= result <= end.
        Side Effects / State:
            Advances the underlying pseudo-random number generator state.
    """
    return randint(start, end)


# Aliases for exact naming match
Randomnumber = random_number
randomnumber = random_number


def main():
    print(random_number(0, 9))


if __name__ == "__main__":
    main()
