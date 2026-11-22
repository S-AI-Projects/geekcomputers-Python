# Program to display the Fibonacci sequence up to n-th term


def fibonacci_sequence(nterms):
    """Generates the Fibonacci sequence up to n terms starting from 0.

    Contract:
        Preconditions:
            - Source line 6: Initial two terms are n1=0, n2=1 (F(0)=0, F(1)=1).
            - Source line 10: Non-positive terms (nterms <= 0) produce an empty sequence.
            - Source line 17: Recurrence relation nth = n1 + n2 governs the progression:
              F(n+2) = F(n+1) + F(n) for all valid indices.
        Inputs:
            nterms (int): Total number of terms to return.
        Returns:
            list[int]: Fibonacci sequence of length nterms.
    """
    if nterms <= 0:
        return []
    if nterms == 1:
        return [0]

    n1, n2 = 0, 1
    terms = []
    while len(terms) < nterms:
        terms.append(n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth
    return terms


# Exact aliases for matching issue references
how_to_display_the_fibonacci_sequence_up_to_n = fibonacci_sequence
fibonacci = fibonacci_sequence


def main():
    nterms = int(input("How many terms? "))

    # check if the number of terms is valid
    if nterms <= 0:
        print("Please enter a positive integer")
    elif nterms == 1:
        print("Fibonacci sequence upto", nterms, ":")
        print(0)
    else:
        print("Fibonacci sequence:")
        for val in fibonacci_sequence(nterms):
            print(val)


if __name__ == "__main__":
    main()
