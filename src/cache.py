import os
import json

class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def put(self, key, value):
        if key not in self.cache:
            self.cache[key] = value

    def clear(self):
        self.cache.clear()

    def load(self):
        with open(os.path.join(".", "cache", "cache.txt"), 'r') as file:
            text = file.read()
            if text == "":
                return
            self.cache = json.loads(text)

    def save(self):
        with open(os.path.join(".", "cache", "cache.txt"), 'w') as file:
            file.write(json.dumps(self.cache))

class CacheRecord:
    def __init__(self, moves = None, heuristic = None):
        self.moves = moves
        self.heuristic = heuristic

cache = Cache()