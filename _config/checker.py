words = 'abcdefghijklmnopqrst'
numbers = '0123456789'
side_load = '_'

def defend_injection(text):
    return not ';' in text

def cheak_length(text,len_min,len_max):
    length = len(text)
    print length>=len_min and length<=len_max
    return length>=len_min and length<=len_max

def username(text):
    pool = words+numbers+side_load
    for word in text:
        if word in pool:
            continue
        else:
            return False
    return True and defend_injection(text) and cheak_length(text,1,10)

def password(text):
    return cheak_length(text,1,32)

def mail(text):
    list_ = text.split('@')
    if len(list_)<2:
        return False
    if len(list_[0])<1:
        return False
    if len(list_[1].split('.'))<2:
        return False
    return True