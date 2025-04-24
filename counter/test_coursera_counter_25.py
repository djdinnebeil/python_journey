import pytest
from unittest.mock import patch, MagicMock
from collections import Counter
from urllib.error import HTTPError, URLError
from multiprocessing.dummy import Pool as ThreadPool

import coursera_counter_25 as count_text2

@patch('urllib.request.urlopen')
def test_valid_response(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = b'Hello world! Hello universe!'
    mock_urlopen.return_value = mock_response

    url = 'https://example.com'
    result = count_text2.download_and_count(url)
    expected = Counter({'hello': 2, 'world': 1, 'universe': 1})
    assert result == expected

def test_invalid_scheme():
    url = 'ftp://example.com'
    result = count_text2.download_and_count(url)
    assert result == Counter()

@patch('urllib.request.urlopen', side_effect=Exception('Something went wrong'))
def test_generic_exception(mock_urlopen):
    url = 'https://example.com'
    result = count_text2.download_and_count(url)
    assert result == Counter()

def test_merge_counters():
    c1 = Counter({'a': 2, 'b': 1})
    c2 = Counter({'a': 1, 'c': 5})
    result = count_text2.merge_counters([c1, c2])
    expected = Counter({'a': 3, 'c': 5, 'b': 1})
    assert result == expected

def test_validation_error():
    url = 'file:///etc/passwd'
    result = count_text2.download_and_count(url)
    assert result == Counter()

@patch('urllib.request.urlopen')
def test_http_error(mock_urlopen):
    mock_urlopen.side_effect = HTTPError(
        url='https://example.com',
        code=404,
        msg='Not Found',
        hdrs=None,
        fp=None
    )
    result = count_text2.download_and_count('https://example.com')
    assert result == Counter()

@patch('urllib.request.urlopen')
def test_url_error(mock_urlopen):
    mock_urlopen.side_effect = URLError('DNS lookup failed')
    result = count_text2.download_and_count('https://example.com')
    assert result == Counter()

def fake_downloader(url):
    return {'python': 3, 'test': 2}

@patch('builtins.print')
def test_main_prints_output(mock_print):
    urls = ['https://fake1', 'https://fake2']
    count_text2.main(urls, download_fn=fake_downloader)
    assert mock_print.call_count >= 1


# Not ideal to do real network calls.
# def test_main_route_runs():
#     urls = [
#         'https://djdinnebeil.github.io/',
#         'https://amatolgame.github.io/'
#     ]
#     count_text2.main(urls)
#     assert True
