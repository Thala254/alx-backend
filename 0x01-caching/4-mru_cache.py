#!/usr/bin/env python3
""" 4-mru_cache module """

BaseCaching = __import__('base_catching').BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class that implements a MRU caching system i.e.
    most recently used - discards most recently used items first
    """
    def __init__(self):
        """
        initializes an instance of MRUCache class
        """
        super().__init__()
        self.usage = []

    def put(self, key, item):
        """
        method that caches a key-value pair in a dictionary
        """
        if key is None or item is None:
            pass
        last_index = len(self.usage) - 1
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
           key not in self.cache_data:
            print(f'DISCARD: {self.usage[last_index]}')
            del self.cache_data[self.usage[last_index]]
            del self.usage[last_index]
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
        return self.cache_data[key]
