# src/func_cache.py
# Caches the return values of a function


# Imports
import hashlib
from functools import partial
from typing import Any


# Definitions
def func_cache():
    """A function wrapper that caches return values based on the arguments
    Just decorate the function, and call it like normal!
    Change history_len to cache more or less return value/arg pairs"""
    
    def decorator(func: callable) -> object:
        """The decorator itself"""
        
        class Wrapper:
            """The wrapper itself"""

            def __init__(self, func: callable) -> None:
                """Create the wrapper"""

                # Set variables
                self._func = func
                self._cache = {}


            def __call__(self, *args, **kwargs) -> Any:
                """Run the function and cache, or return cached value"""
                
                try:
                    out = self._cache[hashlib.new("sha1", str({"args": args, "kwargs": kwargs}).encode()).hexdigest()]
                except KeyError:
                    out = self._func(*args, **kwargs)
                    self._cache[hashlib.new("sha1", str({"args": args, "kwargs": kwargs}).encode()).hexdigest()] = out
                    
                
                return out
            
            def __get__(self, instance, owner) -> partial:
                """Compatibility with objects"""
                
                return partial(self.__call__, instance)
        
        return Wrapper(func)
    
    return decorator