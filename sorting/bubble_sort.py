from typing import List

def bubble_sort_copy(arr: List[int]) -> List[int]:
    """
    Returns a new list containing the elements of the input list sorted in ascending order
    using the Bubble Sort algorithm.

    Args:
        arr (List[int]): The list of integers to sort.

    Returns:
        List[int]: A new list with elements sorted in ascending order.

    Example:
        >>> bubble_sort_copy([3, 1, 4, 2])
        [1, 2, 3, 4]

    Notes:
        - This function does not modify the input list.
        - Bubble Sort is inefficient for large datasets (O(n^2) time).
        - The sort is stable and deterministic.
    """
    sorted_arr = arr.copy()  # Make a shallow copy to avoid mutating the original
    n = len(sorted_arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - 1 - i):
            if sorted_arr[j] > sorted_arr[j + 1]:
                # Swap elements if they are in the wrong order
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True

        # If no elements were swapped in this pass, the list is already sorted
        if not swapped:
            break

    return sorted_arr
