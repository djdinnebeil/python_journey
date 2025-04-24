import unittest
from unittest.mock import patch, MagicMock
from collections import Counter
import io
from urllib.error import HTTPError, URLError

import coursera_counter_25 as count_text2 # assuming your script is named count_text2.py

# Top-level fake downloader function so it's pickleable
def fake_downloader(url):
    return {'python': 3, 'test': 2}

class TestDownloadAndCount(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_valid_response(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'Hello world! Hello universe!'
        mock_urlopen.return_value = mock_response

        url = 'https://example.com'
        result = count_text2.download_and_count(url)
        expected = Counter({'hello': 2, 'world': 1, 'universe': 1})
        self.assertEqual(result, expected)

    def test_invalid_scheme(self):
        url = 'ftp://example.com'
        result = count_text2.download_and_count(url)
        self.assertEqual(result, Counter())

    @patch('urllib.request.urlopen', side_effect=Exception('Something went wrong'))
    def test_generic_exception(self, mock_urlopen):
        url = 'https://example.com'
        result = count_text2.download_and_count(url)
        self.assertEqual(result, Counter())

    def test_merge_counters(self):
        c1 = Counter({'a': 2, 'b': 1})
        c2 = Counter({'a': 1, 'c': 5})
        result = count_text2.merge_counters([c1, c2])
        expected = Counter({'a': 3, 'c': 5, 'b': 1})
        self.assertEqual(result, expected)

    def test_validation_error(self):
        # No patch needed — tests internal validation logic
        url = 'file:///etc/passwd'
        result = count_text2.download_and_count(url)
        self.assertEqual(result, Counter())

    @patch('urllib.request.urlopen')
    def test_http_error(self, mock_urlopen):
        # Simulate a 404 HTTPError
        mock_urlopen.side_effect = HTTPError(
            url='https://example.com',
            code=404,
            msg='Not Found',
            hdrs=None,
            fp=None
        )

        result = count_text2.download_and_count('https://example.com')
        self.assertEqual(result, Counter())

    @patch('urllib.request.urlopen')
    def test_url_error(self, mock_urlopen):
        # Simulate a URLError (e.g., DNS failure)
        mock_urlopen.side_effect = URLError('DNS lookup failed')

        result = count_text2.download_and_count('https://example.com')
        self.assertEqual(result, Counter())

    @patch('builtins.print')
    def test_main_prints_output(self, mock_print):
        urls = ['https://fake1', 'https://fake2']
        count_text2.main(urls, download_fn=fake_downloader)

        self.assertGreaterEqual(mock_print.call_count, 1)

if __name__ == '__main__':
    unittest.main()
