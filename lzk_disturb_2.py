# -*- coding: UTF-8 -*-  
'''
加载需要的包
'''
import json
import jieba
import numpy as np
from pypinyin import lazy_pinyin, Style
from distance_module import doc2vec
from lzk_detect_1 import detect
from lzk_calculate_1 import haha
from random import choice
import random
import collections

def reference_model(model_path='reference_model/mini.ftz', test_args=('你好',)):
    """
    调用参考模型; 需要fasttext
    """
    import fasttext
    model = fasttext.load_model(model_path)
    #print('----Reference model prediction----')
    #print(*test_args, model.predict(*test_args))
    return model.predict(*test_args)

def distance_measure(test_args=(['蓝天白云'], ['白云蓝天'])):
    """
    调用距离计算器; 需要gensim, numpy
    """
    from distance_module import DistanceCalculator
    dc = DistanceCalculator()
    
    return dc(*test_args)

    
def keepclean_opt(zi_list , abuse_zi):
    return [zi for zi in zi_list if zi not in abuse_zi]


def cosine(embedding_array_a , embedding_array_b):
    norm_a = np.linalg.norm(embedding_array_a, axis=1)
    norm_b = np.linalg.norm(embedding_array_b, axis=1)
    cosine_numer = np.multiply(embedding_array_a, embedding_array_b).sum(axis=1)
    cosine_denom = np.multiply(norm_a, norm_b)
    cosine_dist = 1.0 - np.divide(cosine_numer, cosine_denom)
    return cosine_dist
    
    
def most_similar(alter , zi):
    ans = [distance_measure(test_args=([elem],[zi]))['embedding_cosine'] for elem in alter]
    return alter[ans.index(min(ans))]

        
def get_single_word_alter(zi , abuse_yizi , myword):
    #keepclean_opt 确保里面没有脏字
    # 在音似和形似中挑一个embedding最像的
    '''
    '''
    similar_alter = keepclean_opt(myword[zi]['similar'] , abuse_yizi)
    
    #取消上下结构
    if myword[zi]['structure'] == 2 :
        similar_alter = []
    pinyin_alter = keepclean_opt(myword[zi]['pinyin_similar'] , abuse_yizi)
    alter = list(set(pinyin_alter + similar_alter))
    alter.append(lazy_pinyin(zi)[0])
    
    return alter
    
def str_insert(original, new, pos):
    return original[:pos] + new + original[pos:]
    
def insert(string):
    # 分类：
    # string为英文或有中英，优先考虑插入数字或字母。
    # string为全中文，则插入汉字
    # 降低jacarrd词相似度
    # （中文则尽量组词）
    # 优化可以考虑降低字相似度
    #--------------------------------
    #暂时想不出来，用符号和了隔开
    #--------------------------------
    # input : 需要插入的字符串，脏字表
    # output ：所有可能的插入方案
    #
    
    ans = []
    
    #如果重复，长度为2，可以保证cao会被插入caao
    if len(string) > 2 :
        if string.isalnum():
            index = choice(range(1,len(string)-1))
            chongfu = string[index]
            
            #过滤ass的情况
            if string not in str_insert(string,chongfu,index):
                ans.append(str_insert(string,chongfu,index))
            
            #加入括号攻击，亲测可以骗过评测函数
            zuo = choice(range(1,len(string)))
            length = choice(range(1,len(string)-zuo+1))
            substr = string[zuo:zuo+length]
            ans.append(string.replace(substr , '('+substr+')'))
        else :
            #中文，或者中英混合，先考虑插入标点符号
            index = choice(range(1,len(string)))
            ans.append(str_insert(string,"一",index))
            ans.append(str_insert(string,"了",index))
            ans.append(str_insert(string,"*",index))
    
    # sb居然全身而过，算了还是插入汉字吧
    else :
        cha_list = ["刂", "亻", "了", "乜", "厶", "一", "丄", "丅", "丆", "丩", "丷", "乀", "乁", "乄", "乛", "廴"]
        wocha = choice(cha_list)
        index = choice(range(1,len(string)))
        ans.append(str_insert(string,wocha,index))
        ans.append(str_insert(string,"一",index))
        ans.append(str_insert(string,"了",index))
        ans.append(str_insert(string,"*",index))
        
        #专门为sb考虑
        ans.append(string.replace(string[index] , '('+string[index]+')'))
    
    # 备用方案：人为加入骂人的话

    return ans


def recursion(loop , i , attack_num) :
    # 返回所有可能的攻击方式
    # input：
    #   loop :[(key , 循环次数)] 提供嵌套信息和停止递归信息
    #         用来表示key及其对应的替换词序号    
    #   i： 位于loop的第几层
    #   attack_num: 上一层的进攻序列列表
    # output:
    #   new_attack_num_list: 基于这一轮的最终进攻序列列表
    
    new_attack_num_list = []
    
    #最后一位循环 , 不再递归
    if i == len(loop)-1:
        for num in range(loop[i][1]):
            tmp = list(attack_num)
            tmp.append((loop[i][0] , num))
            new_attack_num_list.append(tmp)
            
        return new_attack_num_list
            
    else :
        for num in range(loop[i][1]):
            tmp = list(attack_num)
            tmp.append((loop[i][0] , num))
            back = recursion(loop , i + 1 , tmp)
            for attack in back:
                new_attack_num_list.append(attack)
                
        return new_attack_num_list


def liangchan(alter_dict , line):
    loop = [(key , len(alter_dict[key])) for key in alter_dict.keys()]

    #使用递归实现不知道长度的嵌套循环
    #print('---')
    #print(loop)
    #print('---')
    attack_num_list = recursion(loop , 0 , [])
    #print(attack_num_list)
    #开始生产真实的攻击样本
    ans_list = []
    
    for series in attack_num_list :
    #例子：[('c', 0), ('a', 2), ('o', 4), ('n', 0)]  
        tmp = line
        for item in series :
            if item[0] in tmp:
                tmp = tmp.replace(item[0] , alter_dict[item[0]][item[1]])
        
        if tmp not in ans_list :
            ans_list.append(tmp)
    #print('---')
    #print(ans_list)
    return ans_list
    
def takeSecond(elem):
    return elem[1]
    
def get_rid(alter_dict , model , max_option):
    # 去掉不太符合的替代项
    # 限制：分类器的脏话概率不能为脏话
    #       单项得分去掉一大半
    #print('---get_rid---')
    qudiao = []
    num_option = 8
    
    #先计算攻击规模会不会超过max，如果超过则减半
    base = len(alter_dict.keys())
    while 1 :
        scale = pow(base , num_option)
        if scale > max_option :
            num_option /= 2
    
    
    for yuanshi in alter_dict.keys():
        tmp = list(alter_dict[yuanshi])
        mylist = []
        for gongji in tmp:
            #还是脏话：
            if model.predict(*(gongji,))[0][0] == '__label__1':
                #print('--class:' , gongji)
                continue
            #得到原始分数
            p_score = haha(test_args=([gongji], [yuanshi]))
            mylist.append((gongji , p_score))
        
        #对其进行排序，只要前num_option
        mylist.sort(key = takeSecond , reverse = True)
        alter_dict[yuanshi] = [elem[0] for elem in mylist[:num_option]]
    
        if len(alter_dict[yuanshi]) == 0 :
            qudiao.append(yuanshi)
    
    for qu in qudiao:
        alter_dict.pop(qu)
    
    return alter_dict    
    
def tihuan(string , myword , classify_model , max_option):        
    #随机选择位置并替换，分为字母，数字，汉字情况
    #number_table 也考虑换一些zimu
    ans = []
    change = {}
    number_table = {
        '0':'零',
        '1':'一',
        '2':'二',
        '3':'三',
        '4':'四',
        '5':'五',
        '6':'六',
        '7':'七',
        '8':'八',
        '9':'九',
        'b':['鼻','碧','哔'],
        'f':['法','发','乏'],
        'k':['克','课','刻'],
    }
    
    for i in range(len(string)):
        if string[i].lower() in number_table.keys():
            change[string[i]] = number_table[string[i].lower()]
        elif string[i] in myword.keys():
            tmp = list(set(myword[string[i]]['pinyin_similar'][:5] + myword[string[i]]['similar'][:5]))
            
            #取消上下结构
            zi = string[i]
            if myword[zi]['structure'] == 2 :
                tmp = myword[string[i]]['pinyin_similar'][:10]
            
            change[string[i]] = tmp
    
    #现在开始针对string量产攻击样本
    
    #只替换一处的
    for ti in change.keys():
        for huan in change[ti]:
            ans.append(string.replace(ti , huan))
    
    #检查change
    change = get_rid(change , classify_model, max_option)
    
    #各种替换可能性
    if len(change.keys()) != 0 :
        ans =list(set(ans + liangchan(change , string)))
    
            
    if len(ans) == 0 :
        buquan = random.choice(['二五0','25零','二50' , '2百5'])
        ans.append(buquan)
    return ans
        



    
def disturb(line , token , abuse_yizi , myword , \
            abuse_dict , new_word_dict , classify_model , \
            max_option):
    # 分析:
    # 扰动本质上就2种方式：插入操作和替换操作
    # ---------------------------------------
    # 插入：
    #   适用：序列为1
    #   方式：插入随机汉字，数字，字母
    # 替换：
    #   适用：序列为 1 or 2
    #   方式：替换音似（混淆），形似，拼音（首字母），英文，数字
    # ---------------------------------------
    # 优化的方式有：
    # p值
    # 最小编辑距离；
    # 
    # c值
    # 使用参考模型里最正向的字词扰动
    #
    
    param = {
        'new_word_defense': 0, #新词防守.暂时不实现
        'embedding_opt': 1,    #余弦相似度优化
        'calcost_opt': 1,      #计算扰动成本最优化(暂不考虑词Jacarrd)
        'hunxiaoyin': 0,       #混淆音许可
        'keepclean_opt': 1,    #确保替换不出现脏字
        'preferword_opt': 0,   #倾向于组词。暂时不知道怎么实现
    }
    #加载必要文件
    
    ans = '' # 待定字符串，共第二次标记用
    
    #准备生成多个攻击方法，就靠这个不断替换(从短到长)了
    alter_dict = collections.OrderedDict()
    
    print('第一轮')
    # 第一轮：超脏单字，一定替换
    for i in range(len(token)):
        if token[i] == 2 :
            
            if line[i] not in alter_dict.keys():
                alter = get_single_word_alter(line[i] , abuse_yizi , myword)
                alter_dict[line[i]] = alter
                
            #占位符，保证后面不会出现无辜的识别
            ans = ans + '%'
        else:
            ans = ans + line[i]
    
    
    #第二轮 ：在已经替换超脏字的情况下，继续匹配len>2脏词
    # 前面单个脏字用%token遮住，所以能保证是独立事件
    
    print('第二轮')
    #消除大小写差别
    abuse_dict_1 = [zi.lower() for zi in abuse_dict if len(zi) > 1]
    for zang in abuse_dict_1 :
        if zang in ans.lower() :
            #获取原始字符串ans精准的定位：
            start = ans.lower().index(zang)
            substr = ans[start:start+len(zang)]
            
            if substr not in alter_dict.keys():
                alter = insert(substr) + tihuan(substr, myword , classify_model , max_option)
                
                alter = list(set(alter))
                
                #上述方案要保证识别不出原来脏话，否则alter要被过滤
                tmp = alter
                for item in tmp :
                    if zang in item.lower():
                        alter.remove(item)
                        
                alter_dict[substr] = alter
    
    #---------------------
    #得到原始句子的所有检测部位的所有可能攻击方案
    
    
    '''---------镇坤方案-----------''' 
    #镇坤方案：预筛选出各种方案中不符合要求的攻击样本
    alter_dict = get_rid(alter_dict , classify_model , max_option)
    
    print('第三轮')
    #第三轮：开始利用上面的已知知识，生成各种替换样本
    print(alter_dict)
    print(line)
    if len(alter_dict.keys()) == 0 :
        #没有方案了
        print('没有方案了')
        return []
    else : 
        #return []
        return liangchan(alter_dict , line)
        
       
    
    

def pinyin_attack(line , token , myword ):
    print('--pinyin--')
    tmp = line
    for i in range(len(token)):
        if token[i] == 2:
            line.replace(tmp[i] , lazy_pinyin(tmp[i])[0])
    print(line)
    return line
            
            