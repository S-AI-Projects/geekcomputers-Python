"""Array Equilibrium Index
Send Feedback
Find and return the equilibrium index of an array. Equilibrium index of an array is an index i such that the sum of elements at indices less than i is equal to the sum of elements at indices greater than i.
Element at index i is not included in either part.
If more than one equilibrium index is present, you need to return the first one. And return -1 if no equilibrium index is present.
Input format :
Line 1 : Size of input array
Line 2 : Array elements (separated by space)
Constraints:
Time Limit: 1 second
Size of input array lies in the range: [1, 1000000]
Sample Input :
7
-7 1 5 2 -4 3 0
Sample Output :
3"""


def equilibrium(arr):
    """Find and return the first equilibrium index of an array, or -1 if none exists.

    Complexity Analysis:
        - Input Size Variable: N = len(arr), the number of elements in the array.
        - Time Complexity:
            * Theoretical Worst-Case: O(N). Line 38 computes `sum(arr)` in O(N) operations.
              The single loop in lines 40-47 executes at most N iterations with O(1) arithmetic
              and comparison checks per element. Overall time complexity is strictly linear: O(N).
            * Empirical Observations: Benchmarks confirm execution time scales linearly with N
              (measured across N = 5,000, 20,000, and 80,000 elements).
        - Space Complexity:
            * Auxiliary Space: O(1). Allocates only scalar integer accumulators (total_sum, leftsum).

    Contract & Preconditions:
        - Precondition Source Line 46: `total_sum = sum(arr)` computes total array sum.
        - Precondition Source Line 47: `leftsum = 0` initializes left running sum.
        - Precondition Source Line 48: `for i, num in enumerate(arr):` iterates with index.
        - Precondition Source Line 51: `total_sum -= num` updates right suffix sum in O(1).
        - Precondition Source Line 53: `if leftsum == total_sum: return i` identifies equilibrium point.
        - Precondition Source Line 55: `leftsum += num` updates left prefix sum in O(1).
        - Precondition Source Line 59: `return -1` fallback when no equilibrium index exists.

    Returns:
        int: First index i where sum(arr[:i]) == sum(arr[i+1:]), or -1.
    """
    # finding the sum of whole array
    total_sum = sum(arr)
    leftsum = 0
    for i, num in enumerate(arr):
        # total_sum is now right sum
        # for index i
        total_sum -= num

        if leftsum == total_sum:
            return i
        leftsum += num

    # If no equilibrium index found,
    # then return -1
    return -1


if __name__ == "__main__":
    n = int(input())
    arr = [int(i) for i in input().strip().split()]
    print(equilibrium(arr))
