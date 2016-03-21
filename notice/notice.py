import sys
import time
import hashlib
import requests
import datetime
import base64
import chardet
import json

sys.path.append('..')

from _modules.util.get_text  import *
from _modules.differ.diffmain  import *
from _modules.util.easyLog import *
from _modules.util.mail import *
from _modules.util import *

from _modules.util.mail import *
from _config.database import *

from _modules.util import timer

SCAN_TASKLIST = 60
SIMILARITY = 0.8

now_tasks = []
running_tasks = {}

if __name__ == '__main__':
    while True:
        database.connect()
        users_ = User.select()
        users = []
        for user in users_:
            if user.sideload not in ['(NULL)',None,'None','null']:
                users.append(user)
            else:
                pass
        if len(users) == 0:
            time.sleep(SCAN_TASKLIST)
            database.close()
            continue
        else:
            for user in users:
                now_tasks.append(user.id)
                if user.id not in running_tasks:
                    def task_fun(user_id,user_mail,sideload):
                        Log('Mail: '+user_mail)
                        tid = user_id
                        tasks = json.loads(sideload)['tasks']
                        changed_tasks = []
                        for task_id in tasks:
                            items = Pool.select().where(Pool.tid==task_id).limit(2)
                            if len(items)==2:
                                content_0 = get_text(items[0].data)
                                content_1 = get_text(items[1].data)
                                if similarity(content_0,content_1)<SIMILARITY:
                                    changed_tasks.append(task_id)
                                else:
                                    pass
                        changed_task_urls = []
                        if changed_tasks==[]:
                            Log('Mail: '+user_mail+',no changes.')
                        else:
                            for task_id in changed_tasks:
                                url = Task.select().where(Task.id==task_id)[0].url
                                changed_task_urls.append(url)
                        text = 'When you are not in:\n\n'
                        for url in changed_task_urls:
                            text+='    '
                            text+=url
                            text+='\n'
                        text+='changed.'
                        try:
                            send_mail(user_mail,'Today\'s change.',text)
                            Log('Mail: '+user_mail+' END')
                        except:
                            Log('Mail: '+user_mail+' FAIL')
                    running_tasks[task.id]=timer.AsyncTask(task_fun,(user.id,user.mail,user.sideload),delay_cal(task.every),)
                    running_tasks[task.id].run()
            for tid in running_tasks:
                if tid not in now_tasks:
                    task_ = running_tasks.remove(tid)
                    task_.cancel()
        database.close()
        time.sleep(SCAN_TASKLIST)