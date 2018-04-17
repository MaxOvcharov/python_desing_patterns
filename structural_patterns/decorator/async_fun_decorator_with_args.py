import asyncio
import functools
import time


def timer(repeat_num: int=0, meta: bool=False):
    print(f"START INIT async_timer: {time.time()}")

    def create_timer(func):

        print(f"START INIT create_timer: {time.time()}")
        results = set()

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            ts = time.time()
            print(f'RUN timer: {ts}')
            for _ in range(repeat_num):
                ts2 = time.time()
                await func(*args, **kwargs)
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

    print(f'END INIT async_timer: {time.time()}\n')
    return create_timer


@timer(repeat_num=100, meta=True)
async def list_for_loop():
    await asyncio.sleep(0.000001)
    return [i for i in range(100000)]


async def simple_for_loop():
    res = []
    await asyncio.sleep(0.000001)
    for i in range(100000):
        res.append(i)

    return res


class SimpleCalculator:

    @staticmethod
    @timer(repeat_num=100, meta=True)
    async def sqrt():
        await asyncio.sleep(0.000001)
        return [i*i for i in range(100)]


async def start_decorators():
    print('\nFIRST ASYNC FUNC: ->\n\n')
    await list_for_loop()
    print('\nSECOND ASYNC FUNC: ->\n\n')
    await SimpleCalculator.sqrt()
    print('\nTHIRD ASYNC FUNC: ->\n\n')
    await timer(repeat_num=100, meta=True)(simple_for_loop)()


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_decorators())
    except KeyboardInterrupt as e:
        print(f'Caught keyboard interrupt {e}\nCanceling tasks...')
    finally:
        loop.close()


if __name__ == '__main__':
    main()
