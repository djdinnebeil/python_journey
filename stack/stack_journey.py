class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        else:
            return None

    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def reverse_string(s):
    stack = Stack()
    for char in s:
        stack.push(char)

    reversed_chars = []
    while not stack.is_empty():
        reversed_chars.append(stack.pop())

    return ''.join(reversed_chars)


# if __name__ == '__main__':
#     original = 'Software Engineering'
#     reversed_str = reverse_string(original)
#     print(f'Original: {original}')
#     print(f'Reversed: {reversed_str}')

def is_balanced(expression):
    stack = Stack()
    for char in expression:
        if char == '(':
            stack.push(char)
        elif char == ')':
            if stack.is_empty():
                return False
            stack.pop()
    return stack.is_empty()


if __name__ == '__main__':
    tests = [
        "(a + b) * (c + d)",  # Balanced
        "(((())))",           # Balanced
        "(()",                # Unbalanced
        "())",                # Unbalanced
        "",                   # Balanced
        "())(()",             # Unbalanced
    ]

    for expr in tests:
        print(f"{expr:15} -> {'Balanced' if is_balanced(expr) else 'Unbalanced'}")
