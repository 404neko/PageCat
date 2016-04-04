IGNORE = ['','[](javascript:;) [](javascript:;)','[](javascript:;)']

def remove(list_,items):
    list__ = []
    for i in list_:
        if i in items:
            continue
        list__.append(i)
    return list__

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

def easydiff(str0,str1,ignore=IGNORE,ex=False):
    l0 = str0.replace('\r','').split('\n')
    l1 = str1.replace('\r','').split('\n')
    l0 = remove(l0,ignore)
    l1 = remove(l1,ignore)
    len0 = len(l0)
    len1 = len(l1)
    same = []

def findd(item,list_):
    same = []
    for i in range(len(list_)):
        if list_[i]==item:
            same.append(i)
    return same

def strom(str0,str1,ignore=IGNORE,):
    str0 = mdprebuild(str0)
    str1 = mdprebuild(str1)
    l = str0.replace('\r','').split('\n')
    r = str1.replace('\r','').split('\n')
    l = remove(l,ignore)
    r = remove(r,ignore)
    lenl = len(l)
    lenr = len(r)
    #same = {'l':[],'r':[]}
    for i in range(len(l)):
        if l[i] in r:
            for j in findd(l[i],r):
                r[j]=[r[j],'s']
            l[i]=[l[i],'s']
    return l,r

def cut_(string,by='<br>',length=96):
    new_string = ''
    count = 0
    for char in string:
        new_string+=char
        if count<length:
            count+=1
        else:
            new_string+=by
            count=0
    return new_string

def c2html(l,r,cut=96):
    color = {
        'n':['#f4f7fb','#afb1b4'],
        'a':['#eaffea','#000000'],
        'd':['#ffecec','#000000'],

    }
    sl = '<div style="float: left; width: 50%; background:#afb1b4">'
    sr = '<div style="margin-left: 50%; background:#afb1b4">'
    t = '<div style="background:%s; color:%s">%s</div>\n'
    for item in l:
        if type(item) in [str,unicode]:
            sl+=t % (color['d'][0], color['d'][1], cut_(item), )
        elif type(item)==list:
            item = item[0]
            sl+=t % (color['n'][0], color['n'][1], cut_(item), )
        else:
            pass
    for item in r:
        if type(item) in [str,unicode]:
            sr+=t % (color['a'][0], color['a'][1], cut_(item), )
        elif type(item)==list:
            item = item[0]
            sr+=t % (color['n'][0], color['n'][1], cut_(item), )
        else:
            pass
    sl+='</div>'
    sr+='</div>'
    return sl,sr
'''
str0=open('httpwww.sina.com.cn1459402790.74')
str1=open('httpwww.sina.com.cn1459740591.52')

for i in c2html(*strom(str0.read(),str1.read())):
    print i
'''