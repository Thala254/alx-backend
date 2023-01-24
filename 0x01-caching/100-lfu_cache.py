#!/usr/bin/env python3
""" 100-lfu_cache module """
from base_catching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache class that implements a LFU caching system i.e.
    Least frequently used - discards least often used items first
    """
    def __init__(self):
        """
        initializes an instance of LFUCache class
        """
        super().__init__()
        self.usage = []
        self.frequency = {}

    def put(self, key, item):
        """
        method that caches a key-value pair in a dictionary
        """
        if key is None or item is None:
            pass
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
           key not in self.cache_data:
            lfu = min(self.frequency.values())
            lfu_keys = [k for k, v in self.frequency.items() if v == lfu]

            if len(lfu_keys) > 1:
                lru_lfu = {k: self.usage.index(k) for k in lfu_keys}
                discard = self.usage[min(lru_lfu.values())]
            else:
                discard = lfu_keys[0]

            print(f'DISCARD: {discard}')
            del self.cache_data[discard]
            del self.usage[self.usage.index(discard)]
            del self.frequency[discard]
        # update usage frequency
        self.frequency[key] = self.frequency[key] + 1 if key in self.frequency\
            else 1
        if key in self.usage:
            del self.usage[self.usage.index(key)]
        self.usage.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """
        method that returns the value in self.cache_data linked to key, or None
        """
        if key is None or key not in self.cache_data.keys():
            return None
        del self.usage[self.usage.index(key)]
        self.usage.append(key)
        self.frequency[key] += 1
        return self.cache_data[key]
