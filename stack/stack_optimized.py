class StackFixed():
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        else:
            raise IndexError('cannot pop from empty stack')

    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            raise IndexError('cannot peek from empty stack')

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

# test_stack_fixed.py

