#coding:utf-8
import re

re_text = '>.*?<'

def get_text(string):
    new_texts = []
    for i in re.findall(re_text,string.split('</head>')[-1]):
        if len(i.replace(' ',''))<4:
            pass
        else:
            new_texts.append(i[1:-1])
    return new_texts