import time
import functools


def timer(func):
    print(f"START INIT decorator: {time.time()}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ts = time.time()
        print(f'RUN timer: {ts}')
        res = func(*args, **kwargs)
        te = time.time()
        print(f'STOP timer: {te}')
        print(f'RESULT - {func.__name__!r}: {(te - ts) * 1000:2.4f} ms')
        print('*/*/*' * 10 + '\n')
        return res

    print(f'END INIT decorator: {time.time()}\n')
    return wrapper


@timer
def list_for_loop():
    return [i for i in range(100000)]


def simple_for_loop():
    res = []
    for i in range(100000):
        res.append(i)

    return res


if __name__ == '__main__':
    list_for_loop()
    timer(simple_for_loop)()
