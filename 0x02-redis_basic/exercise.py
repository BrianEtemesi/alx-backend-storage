#!/usr/bin/env python3
"""
defines a function to cache strings
"""
import redis
from uuid import UUID, uuid4
from typing import Union, Callable, Optional

class Cache:
    """
    class representation of an in memory Cache
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Get the data from Redis using the given key. Optionally, use the callable fn
        to convert the data back to the desired format.
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            data = fn(data)

        return data

    def get_str(self, key: str):
        """
        get data from redis as a string using the given key
        """
        return self.get(key, fn=str)

    def get_int(self, key: str):
        """
        get data from redis as an int using given key
        """
        return self.get(key, fn=int)
