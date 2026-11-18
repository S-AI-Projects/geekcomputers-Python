def fib(n):
    """Compute the n-th Fibonacci number recursively using 0-based indexing.

    Inputs:
        n (int): Non-negative integer index in the Fibonacci sequence (0, 1, 2, ...).

    Returns:
        int: The Fibonacci number at index n, where fib(0) = 0, fib(1) = 1, and
             fib(n) = fib(n - 1) + fib(n - 2) for n >= 2.

    Mutation:
        None. The function does not mutate caller state, arguments, or external data.
    """
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
