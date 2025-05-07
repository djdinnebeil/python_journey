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

    # Generate unique indices to remove efficiently using numpy
    num_indices = int(numpy.random.random() * n) + 1
    indices_to_remove = numpy.random.choice(n, size=num_indices, replace=False)

    # Early return if all elements are to be removed
    if len(indices_to_remove) >= len(magic_list):
        print("Magic summation is equal to 0.")
        return 0

    # Efficient list filtering: remove elements at specified indices
    magic_list = [v for i, v in enumerate(magic_list) if i not in indices_to_remove]

    # Calculate the magic summation directly with a generator expression
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
