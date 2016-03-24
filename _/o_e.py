t = 3
c = 0
ti = 5
import sys
import time
sys.path.append('..')
from _modules.util import timer


def delay_call(slot):
    if type(slot)==int:
        return slot
    unit = slot[-1]
    delay = slot[:-1]
    num = {
        'D':24*60*60,
        'H':60*60,
        'M':60,
        'S':1
    }.get(unit,1)
    return int(delay)*num

def oe():
    print 'runned'
    global c
    c+=1
    print c
    if c>t:
        raise TypeError
    else:
        print 'run no err'
    time.sleep(ti)
    return True

running_tasks=timer.AsyncTask(oe,None,delay_call(10),)
running_tasks.run()