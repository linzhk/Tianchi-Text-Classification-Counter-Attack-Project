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
from random import choice
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

def distance_measure(test_args=(['攻击文本'], ['原始文本'])):
    """
    调用距离计算器; 需要gensim, numpy
    """
    from distance_module import DistanceCalculator
    dc = DistanceCalculator()
    
    return dc(*test_args)

def get_p_score(dc):
    p = 3/14 * (1 - dc['normalized_levenshtein'][0])
    p += 1/7 * (1 - dc['jaccard_word'][0])
    p += 3/14 * (1 - dc['jaccard_char'][0])
    p += 3/7 * (1 - dc['embedding_cosine'][0]) 
    return p

def haha(test_args=(['攻击文本'], ['原始文本'])):
    from distance_module import DistanceCalculator
    dc = DistanceCalculator()
    return get_p_score(dc(*test_args))
  


def takeSecond(elem):
    return elem[1]

def calculate(attack_list , line):
    #计算出最高的p值
    #input：
    #   attack_list 所有可能的改动 list
    #   line 原文本
    score_list = []
    
    for attack in attack_list :
        score_list.append(get_p_score(distance_measure(([attack], [line]))))
    
    ans = list(zip(attack_list , score_list))
    
    #这是最大
    return max(ans , key=takeSecond)[0]
    
    #这是排序
    '''
    ans.sort(key=takeSecond)
    if len(ans) == 0 :
        print('wrong!')
    print(ans[-1][0] , ' ' , ans[-1][1])
    return ans[-1][0]
    '''
    
    

def get_c_score(model, test_args=('你好',)):
    """
    调用参考模型; 需要fasttext
    """
    import fasttext
    model = fasttext.load_model(model_path)
    print('----Reference model prediction----')
    print(*test_args, model.predict(*test_args))
    