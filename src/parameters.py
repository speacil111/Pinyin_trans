single_total=355130127  # 一元词频总数
lamda_2=0.99 # 二元模型的权重 0<lamda_2<1
lamda_3=0.99 # 三元模型的权重 0<lamda_3<1
model=2     # 2 or 3
skip_pre_training=True #是否跳过预处理,第一次使用时应设为False
answer_path="../data/std_output.txt" #标准答案路径