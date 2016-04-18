# -*- coding: utf-8 -*-

import os
import sys
import smtplib
import traceback

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

sys.path.append('..' + os.sep + '..')

import _config.mail

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = _config.mail.from_addr
password = _config. mail.password
smtp_server = _config.mail.smtp_server

def send_mail(to_addr,subject,msg,MIME='html',from_addr=from_addr,port=465):#587
    msg = MIMEText(msg, MIME, 'UTF-8')
    msg['From'] = _format_addr(u'Pagecat <%s>' % from_addr)
    msg['To'] = _format_addr(u'User <%s>' % to_addr)
    msg['Subject'] = Header(subject+u' ', 'UTF-8').encode()
    try:
        server = smtplib.SMTP_SSL(smtp_server,port)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        return True
    except Exception,e:
        print traceback.format_exc()
        return False
