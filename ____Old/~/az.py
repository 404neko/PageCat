import time
import hashlib
import requests
from model.diffmain  import *
from model.get_text  import *

path = 'pages/'
temp = 'temp/'

files = []
contents = []
keys = []

import os

for i in os.listdir(path):
    files.append(open(path+i))

for i in files:
    contents.append(get_text(i.read()))
    i.close()
'''
for i in contents:
    keys.append(get_hash(i))

for i in range(0,len(keys)-1):
    print str(i)+'\t'+str(i+1)+'\t'+str(similarity(keys[i],keys[i+1]))
'''
#for i in range(0,len(contents)-1):
#    for j in range(0,max(len(contents[i]),len(contents[i+1]))):
#        print contents[i][j]+'\t'+contents[i+1][j]
for k in range(0,len(contents)-1):
    list0,list1 = filer(contents[k],contents[k+1])
    to_write = ''
    for i in range(0,min(len(list0),len(list1))):
        to_write = to_write+list0[i]+'\t'+list1[i]+'\n'
    to_write+='\n'
    f = open(str(k)+'.txt','wb')
    f.write(to_write)
    f.close()
    '''
    list0,list1 = filer(contents[i],contents[i+1])
    string = ''
    for j in filer(list0,list1):
        for k in j:
            string+=k
            string+=' '
        string+='\n'
    print string'''