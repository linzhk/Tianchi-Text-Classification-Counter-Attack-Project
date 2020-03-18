
import json

def detect(line , abuse_dict):
    """预处理（大小写，去标点），并识别一行文本。

    :param line: 对抗攻击前的输入文本
    :type line: str
    :returns: list -- 012标记序列,和原文本一一对应
                     其中，0代表干净，1代表脏话，2代表脏的来源
                     例如我真是日你妈
                         0 0 0 2 1 2
                         你妈去死吧
                         1 2 1 2 0
    """
        
    
    #去掉\n
    
    line = line.replace('\n', '') 
    token = [0 for i in line]
    
    #标记2 考虑单个汉字
    abuse_dict_2 = [zi for zi in abuse_dict if len(zi) == 1]
    for i in range(len(line)):
        if line[i] in abuse_dict_2 : 
            token[i] = 2
    
    #标记1 考虑大小写
    abuse_dict_1 = [zi.lower() for zi in abuse_dict if len(zi) > 1]
    for zang in abuse_dict_1 :
        if zang in line.lower() :
            index = line.lower().index(zang)
            for i in range(len(zang)):
                if token[index + i] == 2 :
                    continue
                token[index + i] = 1
    
    return (line,token)


def detect_display(line , token):
    """颜色深浅展示被标注效果
        0 没颜色
        1 黄色
        2 蓝色
    :param line: 对抗攻击前的输入文本
           token: 012标记序列，同上函数
    :type line: str
          token:list
    :returns: None
    """
    for i in range(len(line)):
        if token[i] == 0 :
            print(line[i] , end = '')
        elif token[i] == 1 :
            print('\033[1;32;43m'+line[i]+'\033[0m' , end = '')
        elif token[i] == 2 :
            print('\033[1;33;44m'+line[i]+'\033[0m' , end = '')
        else : 
            print('WRONG!!!!!!!')
            break
    print()