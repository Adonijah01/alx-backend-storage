#!/usr/bin/env python3
'''A script containing utilities for caching and monitoring requests.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_cache = redis.Redis()
'''A Redis instance at the module level.
'''


def data_caching_decorator(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invocation_handler(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_cache.incr(f'request_count:{url}')
        result = redis_cache.get(f'response_data:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_cache.set(f'request_count:{url}', 0)
        redis_cache.setex(f'response_data:{url}', 10, result)
        return result
    return invocation_handler


@data_caching_decorator
def fetch_data(url: str) -> str:
    '''Returns the content of a URL after caching the request's response
    and monitoring the request.
    '''
    return requests.get(url).text

