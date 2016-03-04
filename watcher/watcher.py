import sys
import time
import hashlib
import requests
import datetime
import MySQLdb
import base64
import chardet
import timer

sys.path.append('..')

from _models.util.get_text  import *
from _models.differ.diffmain  import *
from _models.util.easyLog import *

from _config.database import *

SCAN_TASKLIST = 60

now_tasks = []
running_tasks = {}

def delay_call(slot):
    unit = slot[-1]
    delay = slot[:-1]
    num = {
        'D':24*60*60,
        'H':60*60,
        'M':60,
        'S':1
    }.get(unit,1)
    return int(delay)*num

if __name__ == '__main__':
    while True:
        tasks = Task.select()
        if len(tasks) == 0:
            time.sleep(SLEEP_NORULE)
            continue
        else:
            for task in tasks:
                now_tasks.append(task.tid)
                if task.tid not in running_tasks:
                    def task_fun():
                        Log('Fetch from: '+task.url)
                        try:
                            content = requests.get(task.url).content
                        except:
                            Log('Fetch fail.')
                        data = Pool(data=content.decode(chardet.detect(content)['encoding'],errors='ignore'),tid=task.tid,time=datetime.datetime.now(),)
                        data.save()
                        #User.update(active=False).where(registration_expired=True)  
                        Task.update(last_update=datetime.datetime.now()).where(Task.tid==task.tid)
                        Log('Fetch from: '+task.url+'....END')
                    running_tasks[task.tid]=timer.loopTimer(delay_call(task.slot),task_fun)
                    running_tasks[task.tid].run()
                    print running_tasks[task.tid]
            for tid in running_tasks:
                if tid not in now_tasks:
                    task_ = running_tasks.remove(tid)
                    task_.cancel()
        time.sleep(SCAN_TASKLIST)
'''
    Log('Process watcher inited.')
    database.connect()
    while 1:
        tasks = Task.select()
        if len(tasks) == 0:
            time.sleep(SLEEP_NORULE)
            continue
        count = LOOP_COUNT
        Log('Got web list.')
        while count:
            for task in tasks:
                Log('Fetch from: '+task.url)
                if True:
                    if slot(task.slot):
                        url = ''.join(task.url.split('#').pop(-1))
                        try:
                            content = requests.get(url).content
                        except:
                            continue
                        #.encode(chardet.detect(content)['encoding'])
                        data = Pool(data=content.decode(chardet.detect(content)['encoding'],errors='ignore'),tid=task.tid,time=datetime.datetime.now(),)
                        data.save()
                        Log('Fetch from: '+task.url+'....END')
                time.sleep(SLEEP_AFTERONEWATCH)
            count-=1
        time.sleep(SLEEP_AFTERLOOP)
'''