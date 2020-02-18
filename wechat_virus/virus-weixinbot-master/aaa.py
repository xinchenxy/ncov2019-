import multiprocessing
import time


if __name__ == '__main__':

    q1 = multiprocessing.Queue(3)
    q1.put(1)
    q1.put(1)
    # q1.put(1)
    time.sleep(0.0000000000000000000001)

    isEmpty = q1.empty()
    print(isEmpty)