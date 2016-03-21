import simhash

def get_hash(string_list):
    return simhash.Simhash(string_list).hash

def make_obj(hash_):
    if type(hash_)==list:
        return simhash.Simhash(hash_)
    elif type(hash_)==int or type(hash_)==long:
        simhash_obj = simhash.Simhash()
        simhash_obj.hash = hash_
        return simhash_obj
    else:
        return hash_

def hamming(hash0,hash1):
    hash0 = make_obj(hash0)
    hash1 = make_obj(hash1)
    return hash0.hamming_distance(hash1)

def similarity(hash0,hash1):
    hash0 = make_obj(hash0)
    hash1 = make_obj(hash1)
    return hash0.similarity(hash1)

def filer(list0,list1):
    list0 = list(set(list0))
    list1 = list(set(list1))
    nlist0 = []
    nlist1 = []
    common = list(set(list0+list1))
    for i in common:
        if (i in list0) and (i not in list1):
            nlist0.append(i)
        if (i in list1) and (i not in list0):
            nlist1.append(i)
    return nlist0,nlist1

