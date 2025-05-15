import time
import random

from crud import get_user_orders_grouped as uncached_get_user_orders_grouped
from crud_cache import get_user_orders_grouped as cached_get_user_orders_grouped
from db_config import db

from crud_cache import user_orders_cache

db.set_session(database_url='sqlite:///caching_test.db')


def measure(fn, label, user_ids):
    """Measure execution time of function fn over list of user_ids."""
    start = time.time()
    for user_id in user_ids:
        fn(user_id)
    end = time.time()
    duration = end - start
    print(f'{label} Duration: {duration:.4f} seconds')
    return duration


def run_scenario(description, user_ids):
    print(f'\n--- Scenario: {description} ---')
    print(f'Total calls: {len(user_ids)} | Unique user_ids: {len(set(user_ids))}')

    random.shuffle(user_ids)
    uncached_ids = user_ids[:]
    cached_ids = user_ids[:]

    uncached_time = measure(uncached_get_user_orders_grouped, '[Uncached]', uncached_ids)

    user_orders_cache.clear()
    user_orders_cache.reset_stats()  # Reset counters

    cached_time = measure(cached_get_user_orders_grouped, '[Cached]', cached_ids)

    stats = user_orders_cache.stats()

    if cached_time > 0:
        speedup = uncached_time / cached_time
        print(f'Speedup Factor: {speedup:.2f}x')
    else:
        print('Cached time too fast to measure accurately.')

    print(f"Cache Hits: {stats['hits']} | Misses: {stats['misses']} | Hit Rate: {stats['hit_rate']}%")

    return {
        'Scenario': description,
        'Uncached Time (s)': round(uncached_time, 4),
        'Cached Time (s)': round(cached_time, 4),
        'Speedup': round(speedup, 2) if cached_time > 0 else float('inf'),
        'Hit Rate (%)': stats['hit_rate']
    }

if __name__ == '__main__':
    print('=== Caching Performance Comparison ===')

    scenarios = [
        ('Repeated Access (High Cache Reuse)', [1, 2, 3, 4, 5] * 200),
        ('Cold Access (No Cache Reuse)', list(range(1, 1001))),
        ('Mixed Access (Some Reuse, Some Evictions)', [random.randint(1, 200) for _ in range(1000)]),
    ]

    results = []

    for description, user_ids in scenarios:
        result = run_scenario(description, user_ids)
        results.append(result)

    print('\n=== Summary Table ===')
    print(f"{'Scenario':<40} | {'Uncached':<8} | {'Cached':<8} | {'Speedup':<8} | {'Hit Rate (%)':<12}")
    print('-' * 80)
    for r in results:
        print(f"{r['Scenario']:<40} | {r['Uncached Time (s)']:<8}s | {r['Cached Time (s)']:<8}s | "
              f"{r['Speedup']:<8}x | {r['Hit Rate (%)']:<12}%")
