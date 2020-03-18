
## 安全AI挑战者计划第三期 - 文本分类对抗攻击比赛方案
### 比赛链接
https://tianchi.aliyun.com/competition/entrance/231762/introduction
### 方案概述和排名
比赛方案为：字典检测+形似字/音似字/拼音/拆字攻击。针对每一条原始样本生成512条攻击候选样本，再选取得分最高的句子作为攻击选项。<br>
整个方案比较关键的是data/mynewword3.json  
他提供了2w字的汉字基本信息（拼音，汉字结构，音似字形似字，拆字，繁体，四角码等）。例如：
```
{"word": "操", "oldword": "撡", "strokes": 16, "pinyin": [["cao1"]], "radicals": "扌", "unicode": "b'64cd'", "chaizi": ["扌", "品", "木"], "is_normal": 1, "sijiao": "56094", "structure": 1, "similar": ["躁", "澡", "燥"], "is_dirty": 0, "pinyin_similar": ["嘈", "漕", "艚", "螬", "糙"], "chaizi_similar": []}
```
需要说明的是，为了尽量保留辱骂性质满足比赛得分条件，形似字只允许左右结构和上下结构的字体。  

以及data/abuse_dict.json和data/abuse_dict_yizi.json。他们主要负责以最小扰动成本识别句子中的脏字。例如：
```
["蛆", "操","垃","圾", "腐", "娘","癞", "淫", "裸", "尿", "死", "揉", "装", "佬", "滥", "癌", "丧", "聋", "嫖", "渴", "干", "炎", "鸡", "妇", "妹", "葬", "骚", "衰", "孬", "废", "币", "虐", "坟", "蠢", "菌", "日", "撒", "病", "贫", "穴", "笨", "捅", "障", "插", "射", "狠", "妈", "啃", "叼", "吊", "倭", "毒", "批", "瞎", "奴", "杂", "肏", "穷", "蝇", "傻", "屌", "畜", "屄", "辱", "精", "痔", "槽", "玛", "渣", "嗲", "猪", "艹", "囡", "母", "泥", "屎", "比", "乳", "怂", "草", "呆", "臊", "滚", "尼", "侮", "遗", "丑", "婊"]
```

最终得分和排名为44 /133.40，参赛人数为1175（rank5%）

### 文件说明
需要安装的包：（python3）。如果不需要利用docker运行，则直接在main.py修改样例然后run即可。
> jieba  
pypinyin  
numpy   
editdistance  
fasttext  
gensim  

此外，你需要从官网下载以下这三个模块：distance_module，reference_model，preprocessing_module，并将其放置于项目路径下。

├── README.md &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 这篇说明文档<br>
├── benchmark_texts.txt &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       | 示例输入文本，用来读取后生成提交结果<br>
├── requirements.txt    &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    | 在此填写需要的Python依赖包<br>
├── main.py  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    | 镜像中执行的Python脚本<br>
├── sanity_check.py    &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 用于检查生成的提交结果文件的脚本<br>
├── Dockerfile         &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  | Docker配置文件<br>
└── run.sh   &nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 执行Python脚本的shell脚本<br>
##### 模型实现
├── lzk_detect_1.py   &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | 标记原始字符串的脏话。2为必改，1为脏话，0为正常<br>
├── lzk_disturb_2.py	&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | 扰动函数，输入标记序列，输出所有可能攻击<br>
├── lzk_calculate_1.py &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  | 根据所有可能(512条)，计算p最高并返回<br>
├── distance_module  &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    | （需要手动下载）比赛方提供的计算[句子相似度模块](https://tianchi.aliyun.com/competition/entrance/231762/information)<br>
├── reference_model   &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | （需要手动下载）比赛方提供的[脏话分类模块](https://tianchi.aliyun.com/competition/entrance/231762/information)<br>
└── preprocessing_module &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| （需要手动下载）比赛方提供的[句子预处理模块](https://tianchi.aliyun.com/competition/entrance/231762/information)<br>
##### 数据
├── small.txt&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;			| 小样本脏话测试<br>
├── data/abuse_dict.json	&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	| 脏话词典<br>
├── data/abuse_dict_yizi.json&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	| 一个字的脏话词典<br>
└── data/mynewword3.json &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		| 汉字词典（包含所有字的形似字，音似字，拆字，部首等信息）<br>



