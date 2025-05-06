def is_palindrome(sentence):
    if not isinstance(sentence, str):
        raise TypeError('Input must be a string')

    left, right = 0, len(sentence) - 1
    while left < right:
        while left < right and not sentence[left].isalpha():
            left += 1
        while left < right and not sentence[right].isalpha():
            right -= 1
        if sentence[left].lower() != sentence[right].lower():
            return False
        left += 1
        right -= 1
    return True


def test_is_palindrome():
    assert is_palindrome('A man, a plan, a canal: Panama') == True
    assert is_palindrome('No lemon, no melon') == True
    assert is_palindrome('Was it a car or a cat I saw?') == True
    assert is_palindrome('Eva, can I see bees in a cave?') == True
    assert is_palindrome('Hello, World!') == False
    assert is_palindrome('RaceCar') == True
    assert is_palindrome('123@#321') == True   # No letters: treated as empty
    assert is_palindrome('!!!') == True        # Only punctuation: treated as empty
    assert is_palindrome('A Toyota’s a Toyota') == True
    assert is_palindrome('palindrome') == False

    try:
        is_palindrome(None)
    except TypeError:
        pass
    else:
        assert False, 'Expected TypeError for None input'

    try:
        is_palindrome(12321)
    except TypeError:
        pass
    else:
        assert False, 'Expected TypeError for numeric input'
