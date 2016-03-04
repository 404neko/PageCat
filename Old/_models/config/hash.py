import hashlib

def uhash(password,salt):
    pre_hash = password[0]+salt+password[1:]
    Hash=hashlib.md5()
    Hash.update(pre_hash)
    return Hash.hexdigest()