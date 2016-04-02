import html2text
import requests
import chardet
import time
import os

def CreatFolder(Path):
    if Path.find('/')==-1:
        if not os.path.exists(Path):
            os.mkdir(Path)
    else:
        Path=Path.split('/')
        Path0=''
        for PathItem in Path:
            Path0=Path0+PathItem+'/'
            if not os.path.exists(Path0):
                os.mkdir(Path0)

def FileNameFiler(String,Replacment=''):
    List=['/','\\','*',':','?','"','<','>','|']
    New=''
    for i in String:
        if i not in List:
            New+=i
        else:
            New+=Replacment
    return New

def rund(url):
    res = requests.get(url)
    con = res.content
    md = html2text.html2text(con.decode(chardet.detect(con)['encoding'],errors='ignore'))
    CreatFolder(FileNameFiler(url))
    file_name = FileNameFiler(url)+os.sep+FileNameFiler(url)+str(time.time())
    f = open(file_name,'wb')
    f.write(md.encode('UTF-8'))
    f.close()
    #print md.encode('UTF-8')

rund('http://www.sohu.com/')
rund('http://www.sina.com.cn/')