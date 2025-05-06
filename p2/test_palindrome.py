import pytest
from palindrome import is_palindrome

@pytest.mark.parametrize("text,expected", [
    ('A man, a plan, a canal: Panama', True),
    ('No lemon, no melon', True),
    ('Was it a car or a cat I saw?', True),
    ('Eva, can I see bees in a cave?', True),
    ('Hello, World!', False),
    ('RaceCar', True),
    ('123@#321', True),   # No letters — treated as empty, so considered True
    ('!!!', True),        # Only punctuation — also considered True
    ('A Toyota’s a Toyota', True),  # Note: ’ is a curly apostrophe, not ignored by isalpha()
    ('palindrome', False),
])
def test_valid_palindromes(text, expected):
    assert is_palindrome(text) == expected

def test_invalid_input_type():
    with pytest.raises(TypeError):
        is_palindrome(None)
    with pytest.raises(TypeError):
        is_palindrome(12321)
    with pytest.raises(TypeError):
        is_palindrome(['A', 'B', 'A'])
