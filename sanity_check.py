import json

with open('adversarial.txt', 'r') as f:
    my_dict = json.loads(f.read())
    assert 'text' in my_dict
    assert isinstance(my_dict['text'], list)
    for _element in my_dict['text']:
        assert isinstance(_element, str)
    print("\n\n----模拟输出检查完成----")
    print("----请上传镜像并提交----")
