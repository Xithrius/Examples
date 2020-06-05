import threading
import time


def func0() -> None:
    time.sleep(3)
    print('Slept for 3 seconds.')


def func1() -> None:
    time.sleep(2)
    print('Slept for 2 seconds.')


threads = []

for func in [func0, func1]:
    threads.append(threading.Thread(None, func, args=()))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
