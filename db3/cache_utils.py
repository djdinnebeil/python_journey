from cachetools import TTLCache

class InstrumentedCache(TTLCache):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hits = 0
        self.misses = 0

    def __getitem__(self, key):
        try:
            result = super().__getitem__(key)
            self.hits += 1
            return result
        except KeyError:
            self.misses += 1
            raise

    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total) * 100 if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': round(hit_rate, 2),
        }

    def reset_stats(self):
        self.hits = 0
        self.misses = 0
