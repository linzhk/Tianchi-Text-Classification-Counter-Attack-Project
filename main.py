# 加载Python自带 或通过pip安装的模块
import random
import jieba
import json
from pypinyin import lazy_pinyin
import fasttext

# 加载用户自己的模块
from lzk_detect_1 import detect, detect_display
from lzk_disturb_2 import disturb , pinyin_attack
from lzk_calculate_1 import calculate
import time

# ----------------------------------------
# 本地调试时使用的路径配置
#inp_path = 'benchmark_texts.txt'
inp_path = 'small.txt'#先拿小文件试试
out_path = 'adversarial.txt'
# ----------------------------------------

# ----------------------------------------
# 提交时使用的路径配置（提交时请激活）
#inp_path = '/tcdata/benchmark_texts.txt'
#out_path = 'adversarial.txt'
# ----------------------------------------

with open(inp_path, 'r', encoding='utf-8') as f:
    inp_lines = f.readlines()
    
with open('data/abuse_dict_yizi.json' , 'r') as f:
    abuse_yizi = json.load(f)
    
with open('data/mynewword3.json','r') as f :
    myword = json.load(f)

with open('data/abuse_dict.json' , 'r') as f:
    abuse_dict = json.load(f)

# 参数：------------------------------
model_path='reference_model/mini.ftz'
classify_model = fasttext.load_model(model_path)
max_option = 100
# ------------------------------------
time_start=time.time()
#得到检测结果
line_token = [detect(_line , abuse_dict) for _line in inp_lines]

time_end=time.time()
print('检测：',time_end-time_start,'s')

#展示检测结果
for _item in line_token :
    detect_display(_item[0] , _item[1])


time_start=time.time()
#得到扰动结果
out_lines = []
new_word_dict = {}
jishu = 0
for _elem in line_token:
    print(jishu)
    jishu += 1
    
    #time
    elem_start=time.time()
    
    #获取各种攻击方式
    ans_list = disturb(_elem[0] , _elem[1] , abuse_yizi ,\
                     myword , abuse_dict , new_word_dict ,\
                     classify_model , max_option)
    
    
    #计算得分最高的
    if len(ans_list) > 0:
        best_attack = calculate(ans_list , _elem[0])
    else :
        #预谋插入主动攻击方法
        
        #这里只用拼音转换代替
        best_attack = pinyin_attack(_elem[0] , _elem[1] , myword)
         
    out_lines.append(best_attack)
    
    
time_end=time.time()
#print('扰动过程：',time_end-time_start,'s')    

target = json.dumps({'text': out_lines}, ensure_ascii=False)

with open(out_path, 'w') as f:
    f.write(target)

print('Finish')

