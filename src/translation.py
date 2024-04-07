import os 
import sys
import json
import numpy as np
import time
from pypinyin import lazy_pinyin
from math import log
import pre_training
import parameters
from read import read_py_ch

single_total=parameters.single_total
lamda_2=parameters.lamda_2
lamda_3=parameters.lamda_3
n=parameters.model
way=parameters.skip_pre_training
answer_path=parameters.answer_path

py_ch_num={}
py_ch_num_tog={}
py_ch_num_trig={}

#改变 getdis 函数计算方式，抛弃py_ch_freq转而使用num.json



def load(n,way):
    global py_ch_num
    global py_ch_num_tog
    global py_ch_num_trig
    if n==2:
        if way:
            with open("../data/py_ch_num.json","r",encoding="utf-8") as file:
                py_ch_num=json.load(file)
            with open("../data/py_ch_num_tog.json","r",encoding="utf-8") as file:
                py_ch_num_tog=json.load(file) 
        else:
            read_py_ch()
            pre_training.pre_processed()
            with open("../data/py_ch_num.json","r",encoding="utf-8") as file:
                py_ch_num=json.load(file)
            with open("../data/py_ch_num_tog.json","r",encoding="utf-8") as file:
                py_ch_num_tog=json.load(file)
    elif n==3:
        if way:
            with open("../data/py_ch_num.json","r",encoding="utf-8") as file:
                py_ch_num=json.load(file)
            with open("../data/py_ch_num_tog.json","r",encoding="utf-8") as file:
                py_ch_num_tog=json.load(file) 
            with open("../data/py_ch_num_trig.json","r",encoding="utf-8") as file:
                py_ch_num_trig=json.load(file)
        else:
            read_py_ch()
            pre_training.pre_processed()
            with open("../data/py_ch_num.json","r",encoding="utf-8") as file:
                py_ch_num=json.load(file)
            with open("../data/py_ch_num_tog.json","r",encoding="utf-8") as file:
                py_ch_num_tog=json.load(file)
            with open("../data/py_ch_num_trig.json","r",encoding="utf-8") as file:
                py_ch_num_trig=json.load(file)
    else:
        print("model取值错误,请检查parameters.py")
        exit(0)  

class each_py():
    def __init__(self,py,ch,dis,prev) -> None:
        self.py=py
        self.ch=ch
        self.dis=dis
        self.prev=prev

def get_dis(py1,py2,ch1,ch2):
    tog_ch=ch1+ch2 
    tog_py=py1+" "+py2
    p1=py_ch_num.get(py1,{}).get(ch1,0)
    counts_2=py_ch_num.get(py2).get(ch2,0)
    if p1>0:
        p2=py_ch_num_tog.get(tog_py,{}).get(tog_ch,0)
        return log(lamda_2*p2/p1+(1-lamda_2)*counts_2/single_total)
    return -100
def get_dis_tri(py1,py2,py3,ch1,ch2,ch3):
    tog_ch=ch1+ch2+ch3 
    tog_py=py1+" "+py2+" "+py3
    ex_py=py1+" "+py2
    ex_ch=ch1+ch2
    p1=py_ch_num_tog.get(ex_py,{}).get(ex_ch,0)
    counts_3=py_ch_num.get(py3,{}).get(ch3,0)
    counts_23=py_ch_num_tog.get(py2+" "+py3,{}).get(ch2+ch3,0)
    if p1>0:
        p2=py_ch_num_trig.get(tog_py,{}).get(tog_ch,0)
        return log(lamda_3*p2/p1+(1-lamda_3)*(lamda_2*counts_23/counts_3+(1-lamda_2)*counts_3/single_total))
    return -100
                        
def viterbi(pinyin):
    output=[]
    layers=[]
    for i in range(len(pinyin)):
        if pinyin[i] not in py_ch_num:
            return ["拼音错误"]
        else:
            if i==0:
                layers.append([each_py(pinyin[i],ch,log(py_ch_num[pinyin[i]].get(ch,1)),None) for ch in py_ch_num[pinyin[i]]])
            else:
                layers.append([each_py(pinyin[i],ch,0,None) for ch in py_ch_num[pinyin[i]]])
                for each in layers[i]:
                    for prevs in layers[i-1]:
                        if prevs ==layers[i-1][0]:
                            each.dis=prevs.dis+get_dis(prevs.py,each.py,prevs.ch,each.ch)
                            each.prev=prevs
                        else:
                            dis_new=prevs.dis+get_dis(prevs.py,each.py,prevs.ch,each.ch)
                            if dis_new>each.dis:
                                each.dis=dis_new
                                each.prev=prevs
        #求最后一层layer里dis最大的节点
    shortest=max(layers[-1],key=lambda x:x.dis)
    while shortest:
        output.append(shortest.ch)
        shortest=shortest.prev
    output=list(reversed(output))
    return output
def viterbi_tri(pinyin):
    output=[]
    layers=[]
    for i in range(len(pinyin)):
        if pinyin[i] not in py_ch_num:
            return ["拼音错误"]
        else:
            if i==0:
                layers.append([each_py(pinyin[i],ch,log(py_ch_num[pinyin[i]].get(ch,1)),None) for ch in py_ch_num[pinyin[i]]])
            elif i==1: #第二层采用二元模型
                layers.append([each_py(pinyin[i],ch,0,None) for ch in py_ch_num[pinyin[i]]])
                for each in layers[i]:
                    for prevs in layers[i-1]:
                        if prevs ==layers[i-1][0]:
                            each.dis=prevs.dis+get_dis(prevs.py,each.py,prevs.ch,each.ch)
                            each.prev=prevs
                        else:
                            dis_new=prevs.dis+get_dis(prevs.py,each.py,prevs.ch,each.ch)
                            if dis_new>each.dis:
                                each.dis=dis_new
                                each.prev=prevs
            else:
                layers.append([each_py(pinyin[i],ch,0,None) for ch in py_ch_num[pinyin[i]]])
                for each in layers[i]:
                    for prevs in layers[i-1]:
                          
                        if prevs ==layers[i-1][0] :
                            first=prevs.prev
                            each.dis=prevs.dis+get_dis_tri(first.py,prevs.py,each.py,first.ch,prevs.ch,each.ch)
                            each.prev=prevs
                        else:
                            first=prevs.prev
                            dis_new=prevs.dis+get_dis_tri(first.py,prevs.py,each.py,first.ch,prevs.ch,each.ch)
                            if dis_new>each.dis:
                                each.dis=dis_new
                                each.prev=prevs
        
                
        #求最后一层layer里dis最大的节点
    shortest=max(layers[-1],key=lambda x:x.dis)
    while shortest:
        output.append(shortest.ch)
        shortest=shortest.prev
    output=list(reversed(output))
    return output        

def py2ch(n,path1="../data/std_input.txt",path2="../data/output.txt"):#多音字问题未解决
    if n==2:
        with open(path1,"r",encoding="utf-8") as infile:
            with open(path2,"w",encoding="utf-8") as outfile: 
                lines=[line.rstrip() for line in infile]
                for line in lines:
                    if line:
                        line=line.lower().split(" ")
                        output=viterbi(line)
                        outfile.write("".join(output)+"\n")
    elif n==3:
        with open(path1,"r",encoding="utf-8") as infile:
            with open(path2,"w",encoding="utf-8") as outfile: 
                lines=[line.rstrip() for line in infile]
                for line in lines:
                    if line:
                        line=line.lower().split(" ")
                        output=viterbi_tri(line)
                        outfile.write("".join(output)+"\n")


def sentences_acc(path1="../data/output.txt",path2=answer_path):
    f1=open(path1,"r",encoding="utf-8")
    f2=open(path2,"r",encoding="utf-8")
    count=0
    correct=0
    for line1,line2 in zip(f1,f2):
        count+=1
        if line1==line2:
            correct+=1
    print("sentences_acc:",correct/count)  

def words_acc(path1="../data/output.txt",path2=answer_path):
    f1=open(path1,"r",encoding="utf-8")
    f2=open(path2,"r",encoding="utf-8")
    count=0
    correct=0
    for line1,line2 in zip(f1,f2):
        line1=line1.rstrip()
        line2=line2.rstrip()
        for ch1,ch2 in zip(line1,line2):
            count+=1
            if ch1==ch2:
                correct+=1
    print("words_acc:",correct/count)      


if __name__ == "__main__":
    load(n,way)
    print("加载完成")
    if len(sys.argv)>1:
        print("开始训练")
        py2ch(n,sys.argv[1],sys.argv[2])
        sentences_acc(sys.argv[2])
        words_acc(sys.argv[2])
    else:
        print("开始训练")
        py2ch(n)
        sentences_acc()
        words_acc()