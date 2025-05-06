import cProfile

def is_prime_optimized(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def sum_of_primes_optimized(numbers):
    total = 0
    for number in numbers:
        if is_prime_optimized(number):
            total += number
    return total


# cProfile.run('sum_of_primes_optimized(numbers)')
# Measure the time taken by the optimized implementation
# start_time = time.time()
# total_optimized = sum_of_primes_optimized(numbers)
# print(f"Optimized Implementation: Sum of primes = {total_optimized}, Time taken = {time.time() - start_time} seconds")

def main():
    numbers = list(range(100000))
    sum_of_primes_optimized(numbers)

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.print_stats(sort='cumulative')