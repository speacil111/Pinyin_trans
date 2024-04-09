import json
import os
import re
from pypinyin import lazy_pinyin
import parameters

py_ch_num={}
py_ch_num_tog={}
py_ch_num_trig={}
single_total=parameters.single_total

def get_source():#附加选做语料库
    raw_data = []
    path = "语料库/sina_news_gbk/"
    path_2 = "语料库/SMP2020/usual_train_new.txt"
    for file in os.listdir(path):
        print("正在处理文件：", file)
        with open(os.path.join(path, file), "r", encoding="GBK", errors="ignore") as file:
            text = file.read()
            sentences=re.split('。|，|！|？|；|：|\n|\r', text)
            for sentence in sentences:
                sen_t=[char for char in sentence if '\u4e00' <= char <= '\u9fa5']
                raw_data.append(sen_t)
    with open(path_2, "r", encoding="GBK", errors="ignore") as sin_file:
        print("正在处理选做文件")
        text = sin_file.read()
        sentences=re.split('。|，|！|？|；|：|\n|\r', text)
        for sentence in sentences:
            sen_t=[char for char in sentence if '\u4e00' <= char <= '\u9fa5']
            raw_data.append(sen_t)
    print("语料库读取完成")
    return raw_data                            
def counts(raw_data):
    counts_1 = {}
    counts_2 = {}
    counts_3 = {}
    print("正在统计")
    for line in raw_data:
        for i in range(len(line)):
            char_1 = line[i]
            counts_1[char_1] = counts_1.get(char_1, 0) + 1
            if i < len(line) - 1:
                char_2 = line[i:i+2]#转换成str
                char_2 ="".join(char_2)
                counts_2[char_2] = counts_2.get(char_2, 0) + 1
            if i < len(line) - 2:
                char_3 = line[i:i+3]
                char_3 = "".join(char_3)
                counts_3[char_3] = counts_3.get(char_3, 0) + 1
    print("统计完成")
    with open("../data/one_counts.json","w",encoding="utf-8") as outfile:
        json.dump(counts_1, outfile, ensure_ascii=False)
    with open("../data/tog_counts.json","w",encoding="utf-8") as outfile:
        json.dump(counts_2, outfile, ensure_ascii=False)
    with open("../data/three_counts.json","w",encoding="utf-8") as outfile:
        json.dump(counts_3, outfile, ensure_ascii=False)



def yiyuan():
    print("正在处理一元拼音与字的对应关系")
    with open("../data/character_table.json","r",encoding="utf-8") as infile:
        ch_table=json.load(infile)
        with open("../data/one_counts.json","r",encoding="utf-8") as file:
            one_counts=json.load(file)
            for key_1 in ch_table:
                for key_2 in ch_table[key_1]:
                    if key_2 in one_counts:
                        if key_1 in py_ch_num:
                            py_ch_num[key_1][key_2]=one_counts[key_2]
                        else:
                            py_ch_num[key_1]={}
                            py_ch_num[key_1][key_2]=one_counts[key_2]
    with open("../data/py_ch_num.json","w",encoding="utf-8") as outfile:
        json.dump(py_ch_num,outfile,ensure_ascii=False)
    print("处理完成")


def eryuan():   #构造二元拼音与字和字的出现次数的对应关系
    print("正在处理二元拼音与字的对应关系")
    with open("../data/tog_counts.json","r",encoding="utf-8") as infile:
        tog_count=json.load(infile)
        for key in tog_count:
            pinyin=lazy_pinyin(key) #返回的是列表
            pinyin=" ".join(pinyin)
            if pinyin in py_ch_num_tog:
                py_ch_num_tog[pinyin][key]=tog_count[key]
            else:
                py_ch_num_tog[pinyin]={}
                py_ch_num_tog[pinyin][key]=tog_count[key]
    with open("../data/py_ch_num_tog.json","w",encoding="utf-8") as outfile:
        json.dump(py_ch_num_tog,outfile,ensure_ascii=False)
    print("处理完成")


def sanyuan():
    print("正在处理三元拼音与字的对应关系")
    with open("../data/three_counts.json","r",encoding="utf-8") as infile:
        three_count=json.load(infile)
        for key in three_count:
            pinyin=lazy_pinyin(key) 
            pinyin=" ".join(pinyin)
            if pinyin in py_ch_num_trig:
                py_ch_num_trig[pinyin][key]=three_count[key]
            else:
                py_ch_num_trig[pinyin]={}
                py_ch_num_trig[pinyin][key]=three_count[key]
    with open("../data/py_ch_num_trig.json","w",encoding="utf-8") as outfile:
        json.dump(py_ch_num_trig,outfile,ensure_ascii=False)
    print("处理完成")
def pre_processed():
    raw_data=get_source()
    counts(raw_data)
    yiyuan()
    eryuan()
    sanyuan()
