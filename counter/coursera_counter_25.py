import urllib.request
import urllib.error
from collections import Counter
import re
from multiprocessing import Pool

MAX_CONTENT_LENGTH = 10_000_000  # 10 MB content limit
TIMEOUT_SECONDS = 10             # Max time to wait for a URL response
TOP_N_WORDS = 152                 # Limit word frequency output

def download_and_count(url):
    try:
        # Validate URL scheme
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f'Unsupported URL scheme: {url}')

        # Request content with a timeout
        response = urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS)

        # Limit how much content is read
        content = response.read(MAX_CONTENT_LENGTH).decode('utf-8', errors='ignore')
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
    total_count = Counter()
    for counter in counters:
        total_count.update(counter)
    return total_count

def main(urls, download_fn=download_and_count):
    with Pool(processes=8) as pool:
        counters = pool.map(download_fn, urls)

    total_word_count = merge_counters(counters)

    print(f'\nTop {TOP_N_WORDS} most common words:\n')
    for word, count in total_word_count.most_common(TOP_N_WORDS):
        print(f'{word}: {count}')

if __name__ == '__main__':
    urls = [
        'https://djdinnebeil.github.io/',
        'https://amatolgame.github.io/'
    ]
    main(urls)
