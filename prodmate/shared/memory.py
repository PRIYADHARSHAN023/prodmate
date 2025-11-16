from sqlitedict import SqliteDict
import time
import os

class LongTermMemory:
    def __init__(self, path=None):
        if path is None:
            path = os.getenv("MEMORY_PATH","/tmp/prodmate_memory.sqlite")
        self.db = SqliteDict(path, autocommit=True)

    def set(self, key, value):
        self.db[key] = {"value": value, "ts": time.time()}

    def get(self, key, default=None):
        item = self.db.get(key)
        return item["value"] if item else default

    def find_prefix(self, prefix):
        return {k:v for k,v in self.db.items() if k.startswith(prefix)}
