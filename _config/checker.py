words = 'abcdefghijklmnopqrst'
numbers = '0123456789'
side_load = '_'

collection = words+numbers+side_load

def username(str):
    if str.find(';')!=-1:
        return False
    for i in str:
        if collection.find(i)==-1:
            return False
        else:
            pass
    return True

def password(str):
    if str.find(';')!=-1:
        return False
    return True

def mail(str):
    if str.find(';')!=-1:
        return False
    str = str.split('@')
    if len(str)!=2:
        return False
    else:
        for i in str[0]:
            if (collection+'.').find(i)==-1:
                return False
            else:
                pass
        if len(str[1].split('.'))<=1:
            return False
                