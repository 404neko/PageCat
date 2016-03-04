import socket
from threading import Thread



class Client:
    
    server_port = 6001
    client_port = 6002
    host='localhost'

    pool = {}
    s = ''

    class Thread(Thread):
        def __init__(self, function, kws):
            super(Thread, self).__init__()
            self.function = function
            self.kws = kws
        def run(self):
            self.function(self.kws)

    def __init__(self,host='localhost',client_port=6001,server_port=6002):
        self.host = host
        self.server_port = server_port
        self.client_port = client_port
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1',server_port))
        self._init_receiver()
        print 00
        #self._receiver()

    def send(self,data):
        self.s.sendto(data,(host,port))

    def _init_receiver(self):
        aThread = self.Thread(self._receiver,4096)
        aThread.run()
        print 11

    def _receiver(self,length = 4096):
        while True:
            buf = self.s.recv(length)
            pool[buf['sync']]=buf


a = Client()