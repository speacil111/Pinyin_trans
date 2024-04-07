import numpy
import pandas as pd
import sys
import os
import re
import json
import string

def read_py_ch():
    character_table={}
    with open("拼音汉字表.txt","r",encoding="GBK") as file:
        lines=[line.rstrip() for line in file]
        for line in lines:
            if line:
                each_line=line.split(' ')
                character=each_line[0]
                words=[]
                for word in each_line[1:]:
                    words.append(word)
                character_table.update({character:words})
    with open("../data/character_table.json","w",encoding="utf-8") as outfile:
        json.dump(character_table,outfile,ensure_ascii=False)


