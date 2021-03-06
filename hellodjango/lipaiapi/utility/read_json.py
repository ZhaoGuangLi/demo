import json
import os
from time import sleep

from lipaiapi.config import BASE_PATH
from lipaiapi.utility.getlogger import GetLogger


log = GetLogger().get_logger()


def read_json_items_value(file_name):
    with open(file_name, encoding="utf-8") as f:
        result = json.load(f)
        list1 = []
        for i in result:
            list2 = []
            for j, k in i.items():
                list2.append(k)
            list1.append(tuple(list2))
        return list1


def read_json_items_key(file):
    with open(file, encoding="utf-8") as f:
        result = json.load(f)
        for i in result:
            list1 = []
            for j, k in i.items():
                list1.append(j)
            return tuple(list1)


def read_json(file_name):
    file_path = BASE_PATH + os.sep + "data" + os.sep + file_name
    with open(file_path, encoding="utf-8") as f:
        result = json.load(f)
        return result


def write_json(data):
    """
    将实际结果写入Json文件
    :param data: 要写入文件的data
    :return: 无
    """
    with open("../testcase/assert_data.json", encoding="utf-8", mode="w") as f:
        f.write(json.dumps(data))
    sleep(1)


def clear_file(file):
    """
    清空文件的内容
    :param file: 文件名
    :return: 无
    """
    with open(file, "r+") as f:
        f.truncate()
    log.info("正在清空文件： {} 的内容".format(file))


if __name__ == '__main__':
    a = 1
    print(a)


