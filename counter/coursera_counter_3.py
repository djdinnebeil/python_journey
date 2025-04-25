import argparse
import urllib.request
import urllib.error
from collections import Counter
import re
from multiprocessing import Pool
import logging

# Configure basic logging format and level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default constants
DEFAULT_MAX_CONTENT_LENGTH = 10_000_000  # Maximum content to read from a URL (in bytes)
DEFAULT_TIMEOUT_SECONDS = 10             # Timeout for URL requests in seconds
DEFAULT_TOP_N_WORDS = 152                # Number of top frequent words to display
DEFAULT_PROCESSES = 8                    # Number of worker processes for multiprocessing

def download_and_count(url):
    """
    Downloads the content of the specified URL and counts word frequencies.

    Parameters:
    - url (str): The URL to download and process.

    Returns:
    - Counter: A Counter object mapping words to their frequency in the downloaded content.
    """
    try:
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f'Unsupported URL scheme: {url}')

        response = urllib.request.urlopen(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        content = response.read(DEFAULT_MAX_CONTENT_LENGTH).decode('utf-8', errors='ignore')

        # Extract words using a regular expression
        words = re.findall(r'\b\w+\b', content.lower())
        return Counter(words)

    except urllib.error.HTTPError as e:
        print(f'HTTP error for {url}: {e.code} - {e.reason}')
    except urllib.error.URLError as e:
        print(f'URL error for {url}: {e.reason}')
    except ValueError as e:
        print(f'Validation error: {e}')
    except Exception as e:
        print(f'Unexpected error processing {url}: {e}')

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

    print(f'\nTop {top_n} most common words:\n')
    for word, count in total_word_count.most_common(top_n):
        print(f'{word}: {count}')

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

    # Example log entry using logging
    logging.info('This is logging.info')

    if not args.urls:
        print('No URLs provided. Example usage:')
        print('  python script.py https://example.com https://example.org')
    else:
        main(args.urls, top_n=args.top, processes=args.processes)
