# 人智导作业一:拼音输入法
## 程序简介：
本程序用来实现拼音到汉字的转换，拼音要求以txt文本形式输入，并且拼音之间带有空格，
程序输出文本文件output.txt,程序运行过程中会产生一些中间文件。

## 操作方法
使用前提：本程序依赖于python库`pypinyin`,请在使用前安装该库

```pip install pypinyin```

**文件夹功能介绍:**

**"src/:"源代码+语料库+拼音汉字表,包含：**

​	"parameters.py":存放参数。

​	"read.py":读取拼音文字表(.txt文件)

​	"pre_training.py":读取语料库数据。

​	"translation.py":主文件，实现拼音输入法

​	语料库文件请放入src文件夹内，具体路径:"src/语料库/sina_news_gbk/xxx.txt"

​	语料库文件夹包含sina_news_gbk文件夹和SMP2020文件夹

​	拼音汉字表请放入src文件夹内，具体路径:"src/拼音汉字表.txt"



**"data/:"测试数据+输出数据+中间文件,包含:**

​	"std_input.txt":测试输入文件

​	"std_output.txt":标准输出答案

​	"output.txt":程序输出

以及各种中间json文件





运行方法: 请先进入src文件夹内，然后在命令行输入`python translation.py ../src/std_input.txt ../src/output.txt`(若使用默认测试文件可以直接输入`python translation.py`)。

特别注意，使用前请务必检查文件是否放置完毕，`parameters.py` 的参数设置是否正确（默认设置是2元输入法+跳过语料库训练，第一次使用请将skip_training改为False）。

此外，本程序输出的句正确率和字正确率所用的文件为std_output.txt,文件路径及其他参数也可以在parameters里更改。

### 测试样例
输入：
```
ji qi xue xi shi dang xia fei chang huo re de ji shu

ren gong zhi neng ji shu fa zhan xun meng

mei ge si nian yi ci de dong ao hui zai jin nian zhao kai le

qing shan lv shui jiu shi jin shan yin shan

zhong guo gong chan dang yuan de chu xin he shi ming shi wei zhong guo ren min mou xing fu wei zhong hua min zu mou fu xing
```
输出:
```
机器学习是当下非常火热的技术

人工智能技术发展迅猛

每个四年一次的冬奥会在今年召开了

青山绿水就是金山银山

中国共产党员的初心和使命是为中国人民谋幸福为中华民族谋复兴
```



注：训练好的json文件已全部打包上传清华云盘，github中不含有这些文件，更多详情请见实验报告。

github地址：https://github.com/speacil111/Pinyin_trans

所有的中间文件已上传清华云盘：https://cloud.tsinghua.edu.cn/d/c36fe9010c6645f5b930/

 