import logging
from logging import Logger

import os
from abc import ABC, abstractmethod


class CacheManager(ABC):
    LOG: Logger = logging.getLogger(__name__)

    @abstractmethod
    def get(self, key: str) -> bytes | None:
        pass

    @abstractmethod
    def set(self, key: str, data: bytes):
        pass


class FsCacheManager(CacheManager):

    def __init__(self, cache_dir: str | None = None):
        self.cache_dir = cache_dir or os.path.expanduser("~/.peaksel/sdk/cache")
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
        CacheManager.LOG.info(f"File system cache initialized in {self.cache_dir}")

    def get(self, key: str) -> bytes | None:
        path = self._get_path(key)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        return None

    def set(self, key: str, data: bytes):
        path = self._get_path(key)
        with open(path, "wb") as f:
            f.write(data)

    def _get_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, key)


class InMemCacheManager(CacheManager):
    def __init__(self):
        self._cache: dict[str, bytes] = {}
        CacheManager.LOG.info(f"In memory cache initialized")

    def get(self, key: str) -> bytes | None:
        return self._cache.get(key)

    def set(self, key: str, data: bytes):
        self._cache[key] = data


class NoCacheManager(CacheManager):

    def get(self, key: str) -> bytes | None:
        return None

    def set(self, key: str, data: bytes):
        pass
