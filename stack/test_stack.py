import pytest
from stack_optimized import StackFixed

def test_push_and_str():
    s = StackFixed()
    s.push(1)
    s.push(2)
    s.push(3)
    assert str(s) == '[1, 2, 3]'

def test_pop_order():
    s = StackFixed()
    s.push('a')
    s.push('b')
    s.push('c')
    assert s.pop() == 'c'
    assert s.pop() == 'b'
    assert s.pop() == 'a'

def test_peek():
    s = StackFixed()
    s.push(99)
    assert s.peek() == 99
    s.push(100)
    assert s.peek() == 100

def test_size():
    s = StackFixed()
    assert s.size() == 0
    s.push('x')
    s.push('y')
    assert s.size() == 2
    s.pop()
    assert s.size() == 1

def test_is_empty():
    s = StackFixed()
    assert s.is_empty() is True
    s.push(5)
    assert s.is_empty() is False
    s.pop()
    assert s.is_empty() is True

def test_pop_empty_raises():
    s = StackFixed()
    with pytest.raises(IndexError, match='cannot pop from empty stack'):
        s.pop()

def test_peek_empty_raises():
    s = StackFixed()
    with pytest.raises(IndexError, match='cannot peek from empty stack'):
        s.peek()
