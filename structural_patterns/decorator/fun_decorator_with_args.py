import functools
import time


def timer(repeat_num: int=0, meta: bool=False):
    print(f"START INIT timer: {time.time()}")

    def create_timer(func):

        print(f"START INIT create_timer: {time.time()}")
        results = set()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ts = time.time()
            print(f'RUN timer: {ts}')
            for _ in range(repeat_num):
                ts2 = time.time()
                func(*args, **kwargs)
                te2 = time.time()
                results.add(float((te2 - ts2) * 1000))

            te = time.time()
            print(f'STOP timer: {te}')
            if meta:
                print(f'RESULT - {func.__name__!r}: ALL CYCLE - {(te - ts) * 1000:2.4f} ms')
                print(f'MIN RESULT: {min(results):2.4f} ms')
                print(f'MAX RESULT: {max(results):2.4f} ms')

            return sum(results) / len(results)

        print(f'END INIT create_timer: {time.time()}\n')
        return wrapper

    print(f'END INIT timer: {time.time()}\n')
    return create_timer


@timer(repeat_num=100, meta=True)
def list_for_loop():
    return [i for i in range(100000)]


def simple_for_loop():
    res = []
    for i in range(100000):
        res.append(i)

    return res


class SimpleCalculator:

    @staticmethod
    @timer(repeat_num=100, meta=True)
    def sqrt():
        return [i*i for i in range(100)]


if __name__ == '__main__':
    print('\nFIRST FUNC: ->\n\n')
    list_for_loop()
    print('\nSECOND FUNC: ->\n\n')
    SimpleCalculator.sqrt()
    print('\nTHIRD FUNC: ->\n\n')
    timer(repeat_num=100, meta=True)(simple_for_loop)()
