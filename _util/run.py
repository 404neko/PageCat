import os
import time
import shutil

path = [
        ['web','main.py'],
        ['mail','mail.py'],
        ['watcher','watcher.py']
]

for item in path:
    if os.path.isfile(item[0]+os.sep+'nohup.out'):
        now = time.strftime('%x%X', time.localtime(time.time()))
        new_name = item[0]+'_'+now.replace('/','').replace(':','')[:-2]+'.log'
        print item[0]+os.sep+'nohup.out',item[0]+os.sep+new_name
        os.rename(item[0]+os.sep+'nohup.out',item[0]+os.sep+new_name)
        shutil.move(item[0]+os.sep+new_name,'log'+os.sep)
for item in path:
    os.system('nohup python %s &',(os.sep.join([item[0],item[1]])))