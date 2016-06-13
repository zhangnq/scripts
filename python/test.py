from multiprocessing import Process
import time
import datetime
import difflib

def doWork():
    while True:
        print "%s: working...." % datetime.datetime.now()
        time.sleep(10)


list=["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","aaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaa","bbbbbbbbbbbbbbbbbbbbbbbbbbbb"]
length=len(list)
i=0
while i<length:
    seq = difflib.SequenceMatcher(None, list[0], result_tmp)


if __name__ == "__main__":
    '''
    p = Process(target=doWork)
    p.start()

    while True:
        time.sleep(3)
        print "%s: ...." % datetime.datetime.now()
    '''