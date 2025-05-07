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

    # Generate unique indices to remove using numpy (0-based indexing)
    num_indices = int(numpy.random.random() * n) + 1
    indices_to_remove = set([int(numpy.random.random() * n) for _ in range(num_indices)])

    # Edge case: All elements are removed
    if len(indices_to_remove) == len(magic_list):
        print("Magic summation is equal to 0.")
        return 0

    for idx in indices_to_remove:
        if 0 <= idx < len(magic_list):
            del magic_list[idx]

    # Transform the list in-place
    for i in range(len(magic_list) - 1):
        magic_list[i] = magic_list[i + 1] // magic_list[i]

    # Calculate the magic summation
    magic_summation_value = sum(magic_list)

    # Print and return the result
    print(f"Magic summation is equal to: {magic_summation_value}.")
    return magic_summation_value

#######################################
####### DO NOT EDIT THIS PART #########
#######################################

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
