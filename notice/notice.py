import sys
import time
import hashlib
import requests
import datetime
import base64
import chardet
import json
import markdown2
import html2text

#pip install markdown2
sys.path.append('..')
sys.path.append('..\..')

from _modules.util.get_text_  import *
from _modules.differ.diffmain  import *
from _modules.differ.stromdiff import *
from _modules.util.easyLog import *
from _modules.util.mail import *
from _modules.util import *

from _modules.util.mail import *
from _config.database import *

from _modules.util import timer

SCAN_TASKLIST = 60
SIMILARITY = 0.95

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
                        database.connect()
                        Log('Mail: '+user_mail)
                        tid = user_id
                        tasks = json.loads(sideload)['tasks']
                        changed_tasks = {}
                        for task_id in tasks:
                            database.connect()
                            items = Pool.select().where(Pool.tid==task_id).limit(2).order_by(Pool.time.desc())
                            if len(items)==2:
                                content_0 = get_text(items[0].data)
                                content_1 = get_text(items[1].data)
                                #print type(content_0), content_0
                                if similarity(content_0,content_1)<SIMILARITY:
                                    old_md = html2text.html2text(items[0].data)
                                    new_md = html2text.html2text(items[1].data)
                                    l,r = strom(old_md,new_md)
                                    text = strom_mail(l,r)
                                    changed_tasks[task_id] = text
                                else:
                                    pass
                        print changed_tasks
                        changed_task_urls = {}
                        if changed_tasks=={}:
                            Log('Mail: '+user_mail+',no changes.')
                            print 'in if'
                            return 0
                        else:
                            for task_id in changed_tasks:
                                url = Task.select().where(Task.id==task_id)[0].url
                                changed_task_urls[url] = changed_tasks[task_id]
                        text = 'When you are not in:\n\n'
                        for url in changed_task_urls:
                            text+='    '
                            text+=url
                            text+=':'
                            text+=markdown2.markdown(changed_task_urls[url])
                            text+='\n'
                        text+='\n'
                        text+='changed.'
                        try:
                            send_mail(user_mail,'Today\'s change.',text)
                            Log('Mail: '+user_mail+' END')
                        except:
                            Log('Mail: '+user_mail+' FAIL')
                        database.close()
                        return 0
                    every = json.loads(user.sideload).get('every',86400)
                    running_tasks[user.id]=timer.AsyncTask(task_fun,(user.id,user.mail,user.sideload),delay_cal(every),)
                    running_tasks[user.id].run()
            for tid in running_tasks:
                if tid not in now_tasks:
                    task_ = running_tasks.remove(tid)
                    task_.stop()
        database.close()
        time.sleep(SCAN_TASKLIST)