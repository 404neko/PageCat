def asplit(arr,one):
    arrs = []
    onearr = []
    for i in arr:
        if len(onearr)!=one:
            onearr.append(i)
        else:
            arrs.append(onearr)
            del onearr
            onearr = []
            continue
    arrs.append(onearr)
    return arrs

ignore = ['','[](javascript:;) [](javascript:;)','[](javascript:;)',')','(']

def remove(list_,items):
    list__ = []
    for i in list_:
        if i in items:
            continue
        list__.append(i)
    return list__

def findd(list_):
    i=-1
    while True:
        try:
            if len(list_[i])>1:
                return list_[i][1]
        except:
            return 0
        i-=1

def easydiff(str0,str1,ignore=ignore,ex=False):
    l0 = str0.replace('\r','').split('\n')
    l1 = str1.replace('\r','').split('\n')
    l0 = remove(l0,ignore)
    l1 = remove(l1,ignore)
    len0 = len(l0)
    len1 = len(l1)
    same = []
    for i in range(len0):
        #if i==418:
        #    print [l0[i]]
        toappend = [i]
        if ex:
            j = findd(same)
            while j<len1:
                if l0[i]==l1[j]:
                    toappend.append(j)
                j+=1
        else:
            for j in range(len1):
                if l0[i]==l1[j]:
                    toappend.append(j)
        same.append(toappend)
    same.append([-1,len1])
    return same,l0,l1

def display(list_):
    l=[]
    r=[]
    for item in list_:
        if not len(item)>1:
            l.append([item[0],'a'])
            r.append(['','n'])
        else:
            l.append([item[0],'n'])
            r.append([item[1],'n'])
    return l,r

def rolling(l,r):
    len_ = len(l)
    roll = 0
    nl = [[0,'n']]
    nr = [[0,'n']]
    for i in range(0,len_):
        if nr[i][0]=='':
            if nr[i-1][0]>roll:
                roll=nr[i-1][0]
            nl.append(l[i])
            r[i][0]=roll
            roll+=1
            r[i][1]='d'
            nr.append(r[i])
        else:
            nl.append(l[i])
            nr.append(r[i])
    last = []
    for i in range(len_):
        if nr[i][0] not in last:
            last.append(nr[i][0])
        else:
            nr[i][0]=''
            nr[i][1]='r'
    return nl,nr

def c2html(nl,nr,l,r):
    color = {
        'n':['#f4f7fb','#afb1b4'],
        'd':['#eaffea','#000000'],
        'a':['#ffecec','#000000'],
        'r':['#f4f7fb','#afb1b4'],

    }
    sl = '<div style="float: left; width: 50%; background:#afb1b4">'
    sr = '<div style="margin-left: 50%; background:#afb1b4">'
    tl = '<div style="background:%s; color:%s">%s</div>\n'
    tr = '<div style="background:%s; color:%s">%s</div>\n'
    len_ = len(nl)
    for i in range(len_):
        try:
            sl+=tl % (color[nl[i][1]][0], color[nl[i][1]][1], l[i])
            sr+=tr % (color[nr[i][1]][0], color[nr[i][1]][1], r[i])
        except:
            pass
    sl+='</div>'
    sr+='</div>'
    return sl,sr

def mdprebuild(string):
    inbrackets = 0
    i=0
    new_string = ''
    while i<len(string):
        if inbrackets:
            if string[i]!=')':
                if string[i] in ['\r','\n']:
                    i+=1
                    continue
                else:
                    new_string+=string[i]
            else:
                new_string+=string[i]
                inbrackets = 0
        else:
            if string[i]=='(':
                inbrackets = 1
                new_string+=string[i]
                i+=1
                continue
            else:
                new_string+=string[i]
        i+=1
    string=new_string
    while i<len(string):
        if inbrackets:
            if string[i]!=']':
                if string[i] in ['\r','\n']:
                    i+=1
                    continue
                else:
                    new_string+=string[i]
            else:
                new_string+=string[i]
                inbrackets = 0
        else:
            if string[i]=='[':
                inbrackets = 1
                new_string+=string[i]
                i+=1
                continue
            else:
                new_string+=string[i]
        i+=1
    return new_string
