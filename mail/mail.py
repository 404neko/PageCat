import sys
import time
import hashlib
import requests
import datetime
import base64
import chardet
import json

sys.path.append('..')

from _models.util.get_text  import *
from _models.differ.diffmain  import *
from _models.util.easyLog import *
from _models.util.mail import *
from _models.util import *

from _models.util.mail import *
from _config.database import *

from _models.util import timer

SCAN_TASKLIST = 60

now_tasks = []
running_tasks = {}

template = {}
template['moniter'] = {'subject':'Notice','msg':'The webpage changes.'}

if __name__ == '__main__':
    while True:
        tasks = MailTask.select()
        if len(tasks) == 0:
            time.sleep(SCAN_TASKLIST)
            continue
        else:
            for task in tasks:
                now_tasks.append(task.id)
                if task.id not in running_tasks:
                    def task_fun():
                        Log('Mail: '+task.mail)
                        tid = task.tid
                        pool_info = Pool.select().where(Pool.tid==tid).limit(2)
                        content_0 = get_text(pool_info[0].data)
                        content_1 = get_text(pool_info[1].data)
                        if similarity(content_0,content_1)<0.8:
                            try:
                                send_mail(task.mail,template[task.template]['subject'],template[task.template]['msg'])
                            except:
                                Log('Mail: Fail')
                            Log('Fetch from: '+task.url+'....END')
                        else:
                            pass
                    running_tasks[task.id]=timer.AsyncTask(task_fun,None,delay_cal(task.every),)
                    running_tasks[task.id].run()
                    #print running_tasks[task.tid]
            for tid in running_tasks:
                if tid not in now_tasks:
                    task_ = running_tasks.remove(tid)
                    task_.cancel()
        time.sleep(SCAN_TASKLIST)