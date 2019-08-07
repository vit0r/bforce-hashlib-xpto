import hashlib
import asyncio
import sys
import time
import concurrent.futures
import traceback
import signal
from pathlib import Path

max_workers = len(hashlib.algorithms_available)
_, xpto, wordlist_file = sys.argv
wordlist_file_lines = Path(wordlist_file).open(mode='r').readlines()


def logging_handler(type, exception, tb):
    traceback_repr = traceback.format_tb(tb)
    print('traceback: {}'.format(traceback_repr))


def create_queue_algorithms():
    for algorithm in hashlib.algorithms_available:
        yield algorithm


def create_hashes(algorithm):
    for word in wordlist_file_lines:
        algorithm_func = hashlib.new(algorithm)
        algorithm_func.update(bytes(word.strip(), 'utf-8'))
        if getattr(algorithm_func, 'hexdigest'):
            hexdigest = str(algorithm_func.hexdigest())
            print('=== {} === \n\n hash: {} \n'.format(algorithm, hexdigest))
            time.sleep(0.5)
            if hexdigest == xpto:
                password_xpto = 'XPTO_PASS: {}'.format(word)
                print(password_xpto)
                Path('password.txt').open(mode='w+').write(password_xpto)


def done_callback(algorithm):
    print('done_callback: ', algorithm)
    time.sleep(3)

def signal_handler():
    loop.stop()
    loop.close()
    sys.exit(1)

async def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as pp_executor:
        future_tasks = {pp_executor.submit(create_hashes, algorithm) for algorithm in create_queue_algorithms()}
        for future_task in future_tasks:
            future_task.add_done_callback(done_callback)


sys.excepthook = logging_handler

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.set_exception_handler(logging_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    loop.run_until_complete(future)
    print('end', time.time() - start)
