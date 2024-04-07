import json
import os
from pypinyin import lazy_pinyin
import parameters

py_ch_num={}
py_ch_num_tog={}
py_ch_num_trig={}
single_total=parameters.single_total

def get_source():#附加选做语料库
    raw_data=[]
    path="语料库/sina_news_gbk/"
    path_2="语料库/SMP2020/usual_train_new.txt"
    for file in os.listdir(path):#判断文件格式
        print("正在处理文件：",file)
        with open(path+file,"r",encoding="GBK",errors="ignore") as sin_file:
            lines=sin_file.readlines()
            for line in lines:
                if line:
                    for char in line:
                        if '\u4e00' <= char <= '\u9fa5':
                            raw_data.append(char)
    with open(path_2,"r",encoding="GBK",errors="ignore") as sin_file: #读取选作语料库
        print("正在处理选做文件")
        lines=sin_file.readlines()
        for line in lines:
            if line:
                for char in line:
                    if '\u4e00' <= char <= '\u9fa5':
                        raw_data.append(char)
    print("语料库读取完成")                            
    return raw_data
def counts_one(processed_data):
    counts={}
    print("正在统计单字")
    for char in processed_data:
        if char in counts:
            counts[char]+=1
        else:
            counts[char]=1
    print("单字统计完成")
    single_total=sum(counts.values())
    print("单字总数：",single_total)       
    with open("../data/one_counts.json","w",encoding="utf-8") as outfile:
        json.dump(counts,outfile,ensure_ascii=False)
def counts_two(processed_data):
    together=[]
    two_counts={}
    print("正在统计2字")
    for char in processed_data:
        together.append(char)
        if len(together)>1:
            tog=together[-2]+together[-1]
            if tog in two_counts:
                two_counts[tog]+=1
            else:
                two_counts[tog]=1
    print("2字统计完成")
    with open("../data/tog_count.json","w",encoding="utf-8") as outfile:
        json.dump(two_counts,outfile,ensure_ascii=False)
def counts_three(processed_data):
    together=[]
    three_counts={}
    print("正在统计3字")
    for char in processed_data:
        together.append(char)
        if len(together)>2:
            tog=together[-3]+together[-2]+together[-1]
            if tog in three_counts:
                three_counts[tog]+=1
            else:
                three_counts[tog]=1
    print("3字统计完成")
    with open("../data/three_count.json","w",encoding="utf-8") as outfile:
        json.dump(three_counts,outfile,ensure_ascii=False)
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
    with open("../data/tog_count.json","r",encoding="utf-8") as infile:
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
    with open("../data/three_count.json","r",encoding="utf-8") as infile:
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
    counts_one(raw_data)
    counts_two(raw_data)
    counts_three(raw_data)
    yiyuan()
    eryuan()
    sanyuan()

