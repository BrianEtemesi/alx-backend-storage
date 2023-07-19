#!/usr/bin/env python3
"""
defines a function to cache strings
"""
import redis
from uuid import UUID, uuid4
from typing import Union

class Cache:
    """
    class representation of an in memory Cache
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

