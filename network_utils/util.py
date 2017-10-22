'''Contain the util for our tools  '''
from time import time

class Timer(object):
    """
    Using : We have 2 ways to handle this timer
    1. Using context manager technic (with .... as
    to start and stop this timer automatically)
    Example :
    with Timer() as my_timer :
        do some thing

    print(my_timer.total)

    2. Create a instance of timer and using his method start,stop
    to handle this timer

    """
    def __init__(self, start_time= None, stop_time= None, auto_start=True):
        self.start_time = start_time
        self.stop_time = stop_time
        if auto_start:
            self.start()

    def start(self):
        self.start_time = self.start_time or round(time(), 2)

    def stop(self):
        self.stoptime = self.stop_time or round(time(), 2)

    @property
    def elapse(self):
        return (time()-self.start_time) if self.start_time else None

    @property
    def total(self):
        return (self.stop_time - self.start_time) \
            if (self.start_time and self.stop_time) else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()