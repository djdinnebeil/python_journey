import sys
import numpy

def magic_summation(n, seed=None):
    ### DO NOT REMOVE OR CHANGE THE COMMAND BELOW
    ### AS IT WON'T BE POSSIBLE TO CORRECTLY GRADE YOUR SOLUTION
    numpy.random.seed(seed)
    if n <= 2:
        return 'n cannot be less than or equal to 2'
    elif not isinstance(n, int):
        return "n must be an integer"

    magic_list = list(range(1, n + 1))  # Convert range to list for Python 3 compatibility
    num_indices = int(numpy.random.random() * n) + 1
    indices_to_remove = set([int(numpy.random.random() * n) for _ in range(num_indices)])

    if len(indices_to_remove) == len(magic_list):
        print("Magic summation is equal to 0.")
        return 0
    def iterator():
        for idx in indices_to_remove:
            if 0 <= idx < len(magic_list):
                del magic_list[idx]
        for i in range(len(magic_list)):
            if i < len(magic_list) - 1:
                magic_list[i] = magic_list[i+1]//magic_list[i]
        for el in magic_list:
            yield el
    it = iterator()
    magic_summation_value = 0
    while True:
        try:
            magic_summation_value += next(it)  # Change it.next() to next(it) for Python 3
        except StopIteration:
            break
    print("Magic summation is equal to: {0}.".format(magic_summation_value))  # Update print statements for Python 3
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