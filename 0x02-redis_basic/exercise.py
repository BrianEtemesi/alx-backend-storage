#!/usr/bin/env python3
"""
defines a function to cache strings
"""
import redis
from uuid import UUID, uuid4
from typing import Union, Callable, Optional
from functools import wraps


def replay(fn: Callable) -> None:
    """
    Displays the call history of a Cache class' method.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    func_name = fn.__qualname__
    in_key = '{}:inputs'.format(func_name)
    out_key = '{}:outputs'.format(func_name)
    func_call_count = 0
    if redis_store.exists(func_name) != 0:
        func_call_count = int(redis_store.get(func_name))
    print('{} was called {} times:'.format(func_name, func_call_count))
    func_inputs = redis_store.lrange(in_key, 0, -1)
    func_outputs = redis_store.lrange(out_key, 0, -1)
    for func_input, func_output in zip(func_inputs, func_outputs):
        print('{}(*{}) -> {}'.format(
            func_name,
            func_input.decode("utf-8"),
            func_output,
        ))


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs):
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a
    particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Append input arguments to the Redis list
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in the Redis list
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


class Cache:
    """
    class representation of an in memory Cache
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Get the data from Redis using the given key. Optionally, use
        the callable fn to convert the data back to the desired format.
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
