import numpy

def magic_summation_original(n, seed=None):
    ### DO NOT REMOVE OR CHANGE THE COMMAND BELOW
    ### AS IT WON'T BE POSSIBLE TO CORRECTLY GRADE YOUR SOLUTION
    ### DO NOT REMOVE OR CHANGE THE COMMAND BELOW
    ### AS IT WON'T BE POSSIBLE TO CORRECTLY GRADE YOUR SOLUTION
    numpy.random.seed(seed)

    # Input validation
    if not isinstance(n, int):
        return "n must be an integer"
    if n <= 2:
        return "n cannot be less than or equal to 2"

    # Create the list [1, 2, ..., n]
    magic_list = list(range(1, n + 1))

    # Generate unique indices to remove
    num_indices = int(numpy.random.random() * n) + 1
    indices_to_remove = set([int(numpy.random.random() * n) for _ in range(num_indices)])

    # Edge case: All elements are removed
    if len(indices_to_remove) == len(magic_list):
        print("Magic summation is equal to 0.")
        return 0

    # Generator function to process magic summation
    def iterator():
        shift = 0  # Track shifting due to deletions
        for idx in sorted(indices_to_remove):
            adjusted_idx = idx - shift  # Adjust for previous deletions
            if 0 <= adjusted_idx < len(magic_list):
                del magic_list[adjusted_idx]
                shift += 1  # Increment shift after deletion

        # Transform the list
        transformed_list = [
            magic_list[i + 1] // magic_list[i] if i < len(magic_list) - 1 else magic_list[i]
            for i in range(len(magic_list))
        ]

        # Yield each transformed element
        yield from transformed_list

    # Sum the yielded values
    it = iterator()
    magic_summation_value = sum(it)

    # print(f"Magic summation is equal to: {magic_summation_value}.")
    return magic_summation_value

def magic_summation_optimized(n, seed=None):
    # Set seed for reproducibility
    numpy.random.seed(seed)

    # Input validation
    if not isinstance(n, int):
        return "n must be an integer"
    if n <= 2:
        return "n cannot be less than or equal to 2"

    # Create the list [1, 2, ..., n]
    magic_list = list(range(1, n + 1))

    # Generate unique indices to remove
    num_indices = int(numpy.random.random() * n) + 1
    indices_to_remove = set([int(numpy.random.random() * n) for _ in range(num_indices)])

    # Edge case: All elements are removed
    if len(indices_to_remove) == len(magic_list):
        print("Magic summation is equal to 0.")
        return 0

    # Deleting elements with correct shifting
    shift = 0
    for idx in sorted(indices_to_remove):
        adjusted_idx = idx - shift
        if 0 <= adjusted_idx < len(magic_list):
            del magic_list[adjusted_idx]
            shift += 1

    # Transform the list in-place
    for i in range(len(magic_list) - 1):
        magic_list[i] = magic_list[i + 1] // magic_list[i]

    magic_summation_value = sum(magic_list)

    # print(f"Magic summation is equal to: {magic_summation_value}.")
    return magic_summation_value

import timeit
import numpy

def run_timing_tests(n, seed, iterations=1000):
    # Timing for the original version
    original_time = timeit.timeit(
        stmt=f'magic_summation_original({n}, {seed})',
        setup='from __main__ import magic_summation_original',
        number=iterations
    )

    # Timing for the optimized version
    optimized_time = timeit.timeit(
        stmt=f'magic_summation_optimized({n}, {seed})',
        setup='from __main__ import magic_summation_optimized',
        number=iterations
    )

    # Print results
    print(f'Number of iterations: {iterations}')
    print(f'Original version average time: {original_time / iterations:.8f} seconds per run')
    print(f'Optimized version average time: {optimized_time / iterations:.8f} seconds per run')
    print(f'Performance improvement: {original_time / optimized_time:.2f}x faster')

# Run timing tests with a sample input
n = 1000
seed = 42
iterations = 1000

print(f'Testing with n={n}, seed={seed}, iterations={iterations}')
run_timing_tests(n, seed, iterations)
