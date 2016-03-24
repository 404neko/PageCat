import sys
import time
import hashlib
import requests
import datetime
import base64
import chardet
import json

sys.path.append('..')

from _modules.util.get_text_  import *
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
                    def task_fun(user_id,user_mail,sideload):
                        Log('Mail: '+user_mail)
                        tid = user_id
                        tasks = json.loads(sideload)['tasks']
                        changed_tasks = []
                        print 'tasks',tasks
                        for task_id in tasks:###
                            items = Pool.select().where(Pool.tid==task_id).limit(2).order_by(Pool.time.desc())
                            if len(items)==2:
                                content_0 = get_text(items[0].data)
                                content_1 = get_text(items[1].data)
                                print 'task_id',task_id,' ',hamming(content_0,content_1),similarity(content_0,content_1)
                                if similarity(content_0,content_1)<SIMILARITY:
                                    changed_tasks.append(task_id)
                                    
                                else:
                                    pass
                        print 'changed_tasks',changed_tasks
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
                            if True:#send_mail(user_mail,'Today\'s change.',text):
                                Log('Mail: '+user_mail+' END')
                            else:
                                Log('Mail: '+user_mail+' FAIL')
                        except:
                            Log('Mail: '+user_mail+' FAIL')
                    task_fun(1,'icedx2008@gmail.com','{"tasks": [4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31], "every": "12H"}')