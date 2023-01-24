#!/usr/bin/env python3
""" 2-lifo_cache module """
from base_catching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class that implements a LIFO caching system i.e.
    Last in first out - cache evicts the block added most recently first.
    """
    def __init__(self):
        """
        initializes an instance of LIFOCache class
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        method that caches a key-value pair in a dictionary
        """
        if key is None or item is None:
            pass
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
           key not in self.cache_data:
            last_index = len(self.order) - 1
            print(f'DISCARD: {self.order[last_index]}')
            del self.cache_data[self.order[last_index]]
            del self.order[last_index]
        self.order.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """
        method that returns the value in self.cache_data linked to key, or None
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
