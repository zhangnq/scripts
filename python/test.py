from multiprocessing import Process
import time
import datetime

def doWork():
    while True:
        print "%s: working...." % datetime.datetime.now()
        time.sleep(10)



if __name__ == "__main__":
    p = Process(target=doWork)
    p.start()

    while True:
        time.sleep(3)
        print "%s: ...." % datetime.datetime.now()