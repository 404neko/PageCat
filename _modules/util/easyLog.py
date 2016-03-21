import time
import sys

eL_Tag={
    'I':'[Info]',
    'W':'[Warning]',
    'E':'[Error]',
    'D':'[Debug]',
    'F':'[Fail]'
    }
cL='['
cR=']'
eL_Joiner=': '
eL_Separator='  '
eL_Newline='\n'

def easyLog(Content,Level='I',TimeFormat='%H:%M:%S',std=sys.stdout,Separator=eL_Separator):
    fTag=eL_Tag.get(Level,Level)
    if TimeFormat=='%H:%M:%S':
        std.write(''.join([cL,time.strftime(TimeFormat,time.localtime(time.time())),cR,Separator,fTag,eL_Joiner,Content,eL_Newline]))
    else:
        try:
            std.write(''.join([cL,time.strftime(TimeFormat,time.localtime(time.time())),cR,Separator,fTag,eL_Joiner,Content,eL_Newline]))
        except:
            std.write(''.join([cL,time.strftime('%H:%M:%S',time.localtime(time.time())),cR,Separator,fTag,eL_Joiner,Content,eL_Newline]))
    return True

def Log(Content,Level='I',TimeFormat='%H:%M:%S',std=sys.stdout,Separator=eL_Separator):
    return easyLog(Content,Level=Level,TimeFormat=TimeFormat,std=std,Separator=Separator)

# Use "from easyLog impoort *"
# and then you can rewrite eL_Tag,cL,cR,eL_Joiner,eL_Separator and eL_Newline
