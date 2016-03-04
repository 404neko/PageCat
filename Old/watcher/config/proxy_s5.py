import socks
import socket

socks.set_default_proxy(socks.SOCKS5, 'localhost', 1080, rdns=True)
socket.socket = socks.socksocket