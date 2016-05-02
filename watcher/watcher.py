import sys
import time
import hashlib
import requests
import datetime
import base64
import chardet
import json

sys.path.append('..')
from _modules.util import timer

from _modules.util.get_text_  import *
from _modules.differ.diffmain  import *
from _modules.util.easyLog import *

from _config.database import *

SCAN_TASKLIST = 60

now_tasks = []
running_tasks = {}

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

if __name__ == '__main__':
    while True:
        database.connect()
        tasks = Task.select()
        for task in tasks:
            if task.active==0:
                now_tasks.remove(task)
        if len(tasks) == 0:
            database.close()
            time.sleep(SCAN_TASKLIST)
            continue
        else:
            for task in tasks:
                if task.active==0:
                    try:
                        now_tasks.remove(task)
                    except:
                        pass
                else:
                    now_tasks.append(task.id)
                #print task.id,'/'len(tasks)
                if task.id not in running_tasks:
                    def task_fun(task_id,task_url):
                        database.connect()
                        Log('Fetch from: '+task_url)
                        try:
                            content = requests.get(task_url).content
                        except:
                            Log('Fetch fail.')
                            return -1
                        data = Pool(data=content.decode(chardet.detect(content)['encoding'],errors='ignore'),tid=task_id,time=datetime.datetime.now(),)
                        data.save()
                        query = Task.update(last_update=datetime.datetime.now()).where(Task.id==task_id)
                        query.execute()
                        last_content = Pool.select().where(Pool.tid==task_id).order_by(Pool.time.desc()).limit(2)
                        '''
                        if len(last_content)==2:
                            old_content = last_content[1].data
                            new_content = last_content[0].data
                            if old_content==new_content:
                                stage = False
                                query = Task.update(news=json.dumps([[],[],stage])).where(Task.id==task_id)
                                query.execute()
                            else:
                                old_list = get_text(old_content)
                                new_list = get_text(new_content)
                                old_list,new_list = filer(old_list,new_list)
                                stage = True
                                query = Task.update(news=json.dumps([old_list,new_list,stage])).where(Task.id==task_id)
                                query.execute()
                        else:
                            pass
                        '''
                        Log('Fetch from: '+task_url+'....END')
                        return 0
                        database.close()
                    running_tasks[task.id]=timer.AsyncTask(task_fun,(task.id,task.url),delay_call(task.slot),)
                    running_tasks[task.id].run()
            for tid in running_tasks:
                if tid not in now_tasks:
                    task_ = running_tasks.remove(tid)
                    task_.stop()
        database.close()
        time.sleep(SCAN_TASKLIST)