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

