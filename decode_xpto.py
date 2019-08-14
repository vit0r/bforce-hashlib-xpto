import hashlib
import asyncio
import concurrent.futures
import traceback
import signal
import aiofiles
from os import sys
from pathlib import Path


max_workers = len(hashlib.algorithms_available)
*_, xpto, wordlist_file = sys.argv


def logging_handler(type, exception, tb):
    traceback_repr = traceback.format_tb(tb)
    print('traceback: {}'.format(traceback_repr))


def create_queue_algorithms():
    yield from hashlib.algorithms_available


def create_hashes(algorithm, wordlist_file_contents):
    for word in wordlist_file_contents:
        algorithm_func = hashlib.new(algorithm)
        algorithm_func.update(bytes(word.strip(), 'utf-8'))
        if getattr(algorithm_func, 'hexdigest'):
            hexdigest = str(algorithm_func.hexdigest())
            if hexdigest == xpto:
                password_xpto = 'Algorithm: {}\nClean password: {}'.format(algorithm, word)
                Path('password.txt').open(mode='w+').write(password_xpto)


def done_callback(future_task):
    if future_task:
        print('done_callback: ', future_task._state)


async def main():
    wordlist_file_contents = None
    async with aiofiles.open(wordlist_file, mode='r') as f:
        wordlist_file_contents = await f.readlines()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as pp_executor:
        future_tasks = {pp_executor.submit(
            create_hashes, algorithm, wordlist_file_contents) for algorithm in create_queue_algorithms()}
        for future_task in future_tasks:
            future_task.add_done_callback(done_callback)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop_policy().get_event_loop()
    #executor = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
    # event_loop.set_default_executor(executor)
    event_loop.set_exception_handler(logging_handler)
    event_loop.set_debug(True)
    event_loop.run_until_complete(main())
    asyncgens = event_loop.shutdown_asyncgens()
    event_loop.run_until_complete(asyncgens)
    event_loop.stop()
    event_loop.close()
    print('event_loop result: ', event_loop._clock_resolution)
