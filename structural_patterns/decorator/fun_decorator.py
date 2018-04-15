import time
import functools
from datetime import datetime


def timer(func):
    print(f"START INIT timer: {time.time()}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ts = time.time()
        print(f'RUN timer: {ts}')
        res = func(*args, **kwargs)
        te = time.time()
        print(f'STOP timer: {te}')
        print(f'RESULT - {func.__name__!r}: {(te - ts) * 1000:2.4f} ms')
        # print('*/*/*' * 10 + '\n')
        return res

    print(f'END INIT timer: {time.time()}\n')
    return wrapper


def logger(func):
    print(f"START INIT logger: {time.time()}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'RUN logger: {time.time()}')
        res = func(*args, **kwargs)
        print(f'LOGGING[{datetime.now()}]: func - {func.__name__} args - {args}, '
              f'kwargs - {kwargs} -> result: {res[:5]}')
        print(f'STOP logger: {time.time()}')
        # print('&/&/&' * 10 + '\n')
        return res

    print(f'END INIT logger: {time.time()}\n')
    return wrapper


@logger
@timer
def list_for_loop():
    return [i for i in range(100000)]


def simple_for_loop():
    res = []
    for i in range(100000):
        res.append(i)

    return res


class SimpleCalculator:

    @staticmethod
    @timer
    @logger
    def sqrt():
        return [i*i for i in range(100)]


if __name__ == '__main__':
    print('\nFIRST FUNC: ->\n\n')
    list_for_loop()
    print('\nSECOND FUNC: ->\n\n')
    SimpleCalculator.sqrt()
    print('\nTHIRD FUNC: ->\n\n')
    timer(simple_for_loop)()
