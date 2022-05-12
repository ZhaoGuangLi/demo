import random
import re


def dict_key(_dict):
    list1 = []
    for i, j in _dict.items():
        if i != "updateTime" and i != "createTime" and i != "updateBy" and i != "createBy":
            list1.append(i)
    return list1


def update_dict(dict1, dict2):
    dict1.update(dict2)
    return dict1


def generate_phone_number():
    """
    生成手机号码
    :return: 手机号码
    """
    condition = None
    while condition is None:
        num = choice_num()
        condition = re.search("^1(3[0-9]|4[0,5-7,9]|5[0-3,5-9]|6[2,5-7]|7[0-8]|8[0-9]|9[0-3,5-9])\d{8}$", num)
    phone_number = int(num)
    return phone_number


def choice_num():
    seq = "1"
    seq1 = "3456789"
    seq2 = "0123456789"
    num = seq + random.choice(seq1)
    for i in range(9):
        num = num + random.choice(seq2)
    return num


def generate_customer_name():
    seq1 = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄"
    seq2 = "小威伟维金光郡立幸招坡披择抬其取若茂苹苗英范东冬冰红琴斑替款堪搭塔越趁趋超提堤博揭喜奏春帮珍玻型封持项城挠政羽秋科重复竿段便俩顺修保促俭俗梅洁静碧璃墙撇嘉摧截誓境摘摔聚暮"
    str1 = ""
    num = random.randint(1, 2)
    for i in range(num):
        str1 = str1 + random.choice(seq2)
    name = random.choice(seq1) + str1
    return name





