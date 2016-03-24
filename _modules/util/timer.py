import time
import threading
import traceback

class AsyncTask:

    def __init__(self,function,args,loop):
        self.function = function
        self.args = args
        self.loop = loop
        self.flag_exit = False
        self.error_c = 0
        self.last = '>'

    def run(self):
        def _run():
            while not self.flag_exit:
                try:
                    if self.args==None:
                        self.function()
                    else:
                        self.function(*self.args)
                except Exception,e:
                    self.last = traceback.format_exc()
                    self.error_c+=1
                    self.error_e = self.last
                    print self.last
                time.sleep(self.loop)
        thread = threading.Thread(target=_run)
        thread.start()

    def error(self):
        return self.error_c,self.last

    def stop(self):
        self.flag_exit = True
