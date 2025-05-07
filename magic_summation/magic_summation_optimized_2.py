import sys
import numpy

def magic_summation(n, seed=None):
    # Set seed for reproducibility
    numpy.random.seed(seed)

    # Input validation
    if not isinstance(n, int):
        return "n must be an integer"
    if n <= 2:
        return "n cannot be less than or equal to 2"

    # Create the list [1, 2, ..., n]
    magic_list = list(range(1, n + 1))

    # Generate unique indices to remove efficiently
    num_indices = int(numpy.random.random() * n) + 1
    indices_to_remove = set(numpy.random.randint(0, n, size=num_indices))

    # Edge case: If all elements are removed
    if len(indices_to_remove) >= len(magic_list):
        print("Magic summation is equal to 0.")
        return 0

    # Efficient list filtering to remove elements at specific indices
    magic_list = [value for idx, value in enumerate(magic_list) if idx not in indices_to_remove]

    # Direct transformation and summation in one step using generator expression
    magic_summation_value = sum(
        (magic_list[i + 1] // magic_list[i] if i < len(magic_list) - 1 else magic_list[i])
        for i in range(len(magic_list))
    )

    # Print and return the result
    print(f"Magic summation is equal to: {magic_summation_value}.")
    return magic_summation_value

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("You must pass at most two arguments, the value for n and/or the random seed")
        sys.exit()
    elif len(sys.argv) == 1:
        print("You must pass at least one argument, the value for n")
        sys.exit()
    elif len(sys.argv) == 3:
        n = int(sys.argv[1])
        seed = int(sys.argv[2])
    else:
        n = int(sys.argv[1])
        seed = None

    magic_summation(n, seed=seed)
