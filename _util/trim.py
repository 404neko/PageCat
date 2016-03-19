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

def trim_fix(uid):
    select_ = User.select().where(User.id==uid)[0]
    sideload = select_.sideload
    mail = select_.mail
    slot = select_.slot
    json_i = json.loads(sideload)
    list_ = json_i['tasks']
    for i in list_:
        print 'Task:',i
        select_ = Task.select().where(Task.id==int(i))[0]
        new_mail_task = MailTask(expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*365*99),\
                                tid=select_.id,\
                                mail=mail,
                                every=_models.util.delay_cal(slot),\
                                template='moniter'
                            )
        new_mail_task.save()
