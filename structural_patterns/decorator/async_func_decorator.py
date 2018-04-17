import asyncio
import functools
import time


def timer(func):
    print(f"START INIT async_timer: {time.time()}")

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        ts = time.time()
        print(f'RUN timer: {ts}')
        res = await func(*args, **kwargs)
        te = time.time()
        print(f'STOP timer: {te}')
        print(f'RESULT - {func.__name__!r}: {(te - ts) * 1000:2.4f} ms')
        return res

    print(f'END INIT async_timer: {time.time()}\n')
    return wrapper


@timer
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
    @timer
    async def sqrt():
        await asyncio.sleep(0.000001)
        return [i*i for i in range(100)]


async def start_decorators():
    print('\nFIRST ASYNC FUNC: ->\n\n')
    await list_for_loop()
    print('\nSECOND ASYNC FUNC: ->\n\n')
    await SimpleCalculator.sqrt()
    print('\nTHIRD ASYNC FUNC: ->\n\n')
    await timer(simple_for_loop)()


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
