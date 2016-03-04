import time
import hashlib
import requests
import datetime
import MySQLdb
import base64

from model.get_text  import *
from model.diffmain  import *
import config.database
from model.easyLog import *

#from _all.proxy_s5 import *

count_main = 0
connect = MySQLdb.connect(config.database.database['host'],config.database.database['user'],config.database.database['password'],config.database.database['database'])

LOOP_COUNT = 32
SLEEP_NORULE = 128
SLEEP_AFTERONEWATCH = 8
SLEEP_AFTERLOOP = 32

def slot(var):
    datedict = eval(datetime.datetime.now().strftime('{\'Y\':\'%Y\',\'M\':\'%m\',\'D\':\'%d\',\'H\':\'%H\',\'M\':\'%M\',\'S\':\'%S\'}'))
    every = var[:2]
    t = var[-1]
    def f(x):
        if x==0:
            return False
        else:
            return True
    if t=='L':
        return True
    else:
        return f(int(int(datedict[t])%int(every)))

Log('Process watcher inited.')
while 1:
    cursor_r = connect.cursor()
    cursor_w = connect.cursor()
    exec_count = cursor_r.execute('SELECT * FROM `fetch`.`watcher`')
    Log('Get web list.')
    if exec_count == 0:
        time.sleep(SLEEP_NORULE)
        continue
    count = LOOP_COUNT
    Log('Got web list.')
    while count:
        cursor_r.execute('SELECT * FROM `fetch`.`watcher`')
        watchers = cursor_r.fetchall()
        for watcher in watchers:
            Log('Fetch from: '+watcher[0])
            if watcher[3]:
                if slot(watcher[2]):
                    url = ''.join(watcher[0].split('#').pop(-1))
                    try:
                        content = requests.get(url).content
                    except:
                        continue
                    keys = '['
                    for i in get_text(content):
                        keys+='\''
                        keys+=i
                        keys+='\','
                    keys += ']'
                    cursor_w.execute('INSERT INTO `fetch`.`pool` (`page`,`wid`,`keys`,`hash`) VALUES (%s, %s, %s, %s);',(content, watcher[1],keys,str(get_hash(content))))
                    connect.commit()
                    Log('Fetch from: '+watcher[0]+'....END')
            time.sleep(SLEEP_AFTERONEWATCH)
        count-=1
    time.sleep(SLEEP_AFTERLOOP)