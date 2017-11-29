'''Contain the util for our tools  '''
import logging
import os
import signal

from time import time

import gevent

log = logging.getLogger(__name__)

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
        log.info('start timer')
        self.start_time = self.start_time or round(time(), 2)

    def stop(self):
        log.info('stop timer')
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

"""Boostraping code."""

def run_until_terminated(cleanup=None, timeout=3.0):
    """Keep the application alive until interrupted.

    Rememeber to use this method in main thread .
    This method  will be interupted if either the SIGTERM
    or SIGINT are trapped. On termination, if a cleanup callable
    was passed in, it will be called with the supplied keyword arguments.

    Args:
        cleanup : A callable method which should be executed to release any
        resources.

        timeout : The maxium of seconds to wait for the cleanup method to complete
        before  forceably killing that greenlet
    """

    def terminate(signum):
        log.info('Terminating with signal %s', signum)

        if cleanup:
            log.debug('Clean up')

            cleanup_greenlet = gevent.spawn(cleanup, signum)
            cleanup_greenlet.join(timeout=timeout)
            cleanup_greenlet.kill()

        run_until_terminated.stopped = True

        kill_signal = signal.SIGKILL
        if 'COVERAGE' in os.environ:
            kill_signal = signal.SIGTERM
        os.kill(os.getpid(),kill_signal)

    # Start 2 greenlet to handle the signal
    gevent.signal(signal.SIGTERM,terminate, signal.SIGTERM)
    gevent.signal(signal.SIGINT, terminate, signal.SIGINT)

    while not run_until_terminated.stopped:
        gevent.sleep(1)

# set this attribute default False when import it
run_until_terminated.stopped = False