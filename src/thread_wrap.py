# src/thread_wrap.py
# Contains a function wrapper that turns it into a thread


# Imports
from functools import partial
from threading import Thread


# Definitions
def thread_wrap(thread_name: str):
    """A function wrapper that turns it into a thread
    Just decorate the function, and call it like normal!"""
    
    def decorator(func):
        """The decorator itself"""
        
        class Wrapper(Thread):
            """The wrapper itself"""

            def __init__(self, func) -> None:
                """Create the wrapper"""

                # Set variables
                self._func = func
                self._thread_name = thread_name


            def __call__(self, *args, **kwargs):

                # Initialize the thread
                super().__init__(target=self._func, name=self._thread_name, args=args, kwargs=kwargs)

                # Start the thread
                self.start()
            
            
            def __get__(self, instance, owner):
                return partial(self.__call__, instance)
        
        return Wrapper(func)
    
    return decorator