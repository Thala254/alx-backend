#!/usr/bin/env python3
""" First-in-first-out cache module """
from base_catching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class that implements a FIFO caching system i.e.
    First in first out - cache evicts the blocks in the order they were added.
    """
    def __init__(self):
        """
        initializes an instance of FIFOCache class
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
            print(f'DISCARD: {self.order[0]}')
            del self.cache_data[self.order[0]]
            del self.order[0]
        self.order.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """
        method that returns the value in self.cache_data linked to key, or None
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
