import sys
import time
import hashlib
import requests
import datetime
import base64
import chardet
import json

sys.path.append('..')
from _models.util import timer

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
        database.connect()
        tasks = Task.select()
        if len(tasks) == 0:
            time.sleep(SCAN_TASKLIST)
            continue
        else:
            for task in tasks:
                now_tasks.append(task.id)
                if task.id not in running_tasks:
                    def task_fun():
                        Log('Fetch from: '+task.url)
                        try:
                            content = requests.get(task.url).content
                        except:
                            Log('Fetch fail.')
                            return -1
                        data = Pool(data=content.decode(chardet.detect(content)['encoding'],errors='ignore'),tid=task.id,time=datetime.datetime.now(),)
                        data.save()
                        query = Task.update(last_update=datetime.datetime.now()).where(Task.id==task.id)
                        query.execute()
                        last_content = Pool.select().where(Pool.tid==task.id).order_by(Pool.time.desc()).limit(2)
                        if len(last_content)==2:
                            if old_content==new_content:
                                stage = False
                                query = Task.update(news=json.dumps([[],[],stage])).where(Task.id==task.id)
                                query.execute()
                            else:
                                old_content = last_content[1].data
                                new_content = last_content[0].data
                                old_list = get_text(old_content)
                                new_list = get_text(new_content)
                                old_list,new_list = filer(old_list,new_list)
                                stage = True
                                query = Task.update(news=json.dumps([old_list,new_list,stage])).where(Task.id==task.id)
                                query.execute()
                        else:
                            pass
                        Log('Fetch from: '+task.url+'....END')
                        return 0
                    running_tasks[task.id]=timer.AsyncTask(task_fun,None,delay_call(task.slot),)
                    running_tasks[task.id].run()
            for tid in running_tasks:
                if tid not in now_tasks:
                    task_ = running_tasks.remove(tid)
                    task_.cancel()
        database.close()
        time.sleep(SCAN_TASKLIST)