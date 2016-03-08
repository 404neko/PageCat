import socket
import json
import random

server_port = 6001
client_port = 6002

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1',server_port))

db = {}

def dput(key,value):
    db[key] = value
    return True

while True:
    rand = str(int(random.random()*1000000))
    try:
        data, addr = s.recvfrom(1024)
        json_ = json.loads(data)
        command = json_['action']
        try:
            group = json_['group']
        except:
            group = 'main'

        if command == 'put':
            putd = False
            while not putd:
                if 'main'+rand not in db:
                    dput('main'+rand,json_['data'])
                    putd = True
                else:
                    rand = str(int(random.random()*1000000))
            respon = {'success':True,'key':'main'+rand,'sync':json_['sync']}
            s.sendto(json.dumps(respon))

        if command == 'get':
            value = db.get(json_['key'],None)
            respon = {'success':True,'value':value,'sync':json_['sync']}
            s.sendto(json.dumps(respon))

        if command == 'pop':
            value = db.pop(json_['key'],None)
            respon = {'success':True,'value':value,'sync':json_['sync']}
            s.sendto(json.dumps(respon))

        if command == 'print':
            value = db.get(json_['key'],None)
            print data, addr, '--',json_['key'],':',value
            respon = {'success':True,'sync':json_['sync']}
            s.sendto(json.dumps(respon))

        if command == 'clear':
            #async
            for i in db:
                if i.find(json_['group'])!=-1:
                    db.pop(i)
            respon = {'success':True,'sync':json_['sync']}
            s.sendto(json.dumps(respon))
    except:
        pass