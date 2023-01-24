#!/usr/bin/python3
""" 3-lru_cache module """

BaseCaching = __import__('base_catching').BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class that implements a LRU caching system i.e.
    least recently used - discards the least recently used items first
    """
    def __init__(self):
        """
        initializes an instance of LRUCache class
        """
        super().__init__()
        self.usage = []

    def put(self, key, item):
        """
        method that caches a key-value pair in a dictionary
        """
        if key is None or item is None:
            pass
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
           key not in self.cache_data:
            print(f'DISCARD: {self.usage[0]}')
            del self.cache_data[self.usage[0]]
            del self.usage[0]
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
