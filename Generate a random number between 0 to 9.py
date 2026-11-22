# Program to generate a random number between 0 and 9

# importing the random module
import random


def generate_random_number(start=0, end=9, rng=None):
    """Return a random integer N such that start <= N <= end.

    Precondition (source: line 6 – ``random.randint(start, end)``):
        start <= end  (violated inputs raise ValueError from randint)

    Args:
        start: Lower bound of the range (inclusive).  Default 0.
        end:   Upper bound of the range (inclusive).  Default 9.
        rng:   Object with a ``randint(a, b)`` method.  Defaults to the
               ``random`` standard-library module (dependency injection for
               testability).

    Returns:
        int in [start, end].

    Raises:
        ValueError: When start > end (delegated from random.randint).
    """
    if rng is None:
        rng = random
    return rng.randint(start, end)


if __name__ == "__main__":
    print(generate_random_number())
