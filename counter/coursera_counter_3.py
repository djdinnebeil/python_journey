import argparse
import urllib.request
import urllib.error
from urllib.parse import urlparse
from collections import Counter
import re
from multiprocessing import Pool
import logging
import sys

# Configure basic logging_python format and level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print_logger = logging.getLogger('print_logger')
print_handler = logging.StreamHandler(sys.stdout)
print_handler.setFormatter(logging.Formatter('%(message)s'))
print_logger.addHandler(print_handler)
print_logger.setLevel(logging.INFO)
print_logger.propagate = False

# Default constants
DEFAULT_MAX_CONTENT_LENGTH = 10_000_000  # Maximum content to read from a URL (in bytes)
DEFAULT_TIMEOUT_SECONDS = 10             # Timeout for URL requests in seconds
DEFAULT_TOP_N_WORDS = 152                # Number of top frequent words to display
DEFAULT_PROCESSES = 8                    # Number of worker processes for multiprocessing

def is_valid_http_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ('http', 'https') and bool(result.netloc)
    except ValueError:
        return False

def download_and_count(url):
    """
    Downloads the content of the specified URL and counts word frequencies.

    Parameters:
    - url (str): The URL to download and process.

    Returns:
    - Counter: A Counter object mapping words to their frequency in the downloaded content.
    """
    if not is_valid_http_url(url):
        logging.error(f'Invalid url: {url}')
        return Counter()
    try:
        response = urllib.request.urlopen(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        content = response.read(DEFAULT_MAX_CONTENT_LENGTH).decode('utf-8', errors='ignore')
        # Extract words using a regular expression
        words = re.findall(r'\b\w+\b', content.lower())
        return Counter(words)

    except urllib.error.HTTPError as e:
        logging.error(f'HTTP error for {url}: {e.code} - {e.reason}')
    except urllib.error.URLError as e:
        logging.error(f'URL error for {url}: {e.reason}')
    except ValueError as e:
        logging.error(f'Validation error: {e}')
    except Exception as e:
        logging.error(f'Unexpected error processing {url}: {e}')

    return Counter()

def merge_counters(counters):
    """
    Merges multiple Counter objects into one.

    Parameters:
    - counters (list of Counter): A list of Counter objects to be combined.

    Returns:
    - Counter: A single Counter with aggregated word counts.
    """
    total_count = Counter()
    for counter in counters:
        total_count.update(counter)
    return total_count

def main(urls, top_n=DEFAULT_TOP_N_WORDS, processes=DEFAULT_PROCESSES, download_fn=download_and_count):
    """
    Coordinates the download and word count process using multiprocessing.

    Parameters:
    - urls (list of str): List of URLs to process.
    - top_n (int): Number of top words to display.
    - processes (int): Number of worker processes to use.
    - download_fn (callable): Function to download and count words (can be overridden for testing).
    """
    # Use a process pool to fetch and count words concurrently
    with Pool(processes=processes) as pool:
        counters = pool.map(download_fn, urls)

    # Merge all individual counters into one
    total_word_count = merge_counters(counters)

    print_logger.info(f'\nTop {top_n} most common words:\n')
    for word, count in total_word_count.most_common(top_n):
        print_logger.info(f'{word}: {count}')

if __name__ == '__main__':
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description='Count the most common words across multiple web pages.'
    )
    parser.add_argument(
        'urls',
        nargs='*',
        help='List of URLs to fetch and analyze (space-separated)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=DEFAULT_TOP_N_WORDS,
        help=f'Number of top words to display (default: {DEFAULT_TOP_N_WORDS})'
    )
    parser.add_argument(
        '--processes',
        type=int,
        default=DEFAULT_PROCESSES,
        help=f'Number of worker processes to use (default: {DEFAULT_PROCESSES})'
    )

    args = parser.parse_args()

    if not args.urls:
        args.urls = ['https://djdinnebeil.github.io']
        main(args.urls, top_n=args.top, processes=args.processes)
    else:
        main(args.urls, top_n=args.top, processes=args.processes)

    logger.info('End of program')