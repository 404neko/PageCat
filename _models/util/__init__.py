import re

def check_url(url):
    if url==None:
        return False
    if url[:5] not in ['http:','https']:
        return False
    else:
        return True

def true_url(url):
    return url.split('#')[0] 

def delay_cal(slot):
    if type(slot)==int:
        return slot
    unit = slot[-1]
    delay = slot[:-1]
    num = {
        'D':24*60*60,
        'H':60*60,
        'M':60,
        'S':1
    }.get(unit,1)
    return int(delay)*num