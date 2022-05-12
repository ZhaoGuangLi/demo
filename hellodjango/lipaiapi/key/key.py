import json
import re
import requests
import lipaiapi.key
from lipaiapi.utility.common import update_dict
from lipaiapi.utility.getlogger import GetLogger
import ddddocr


class Key:
    ocr = ddddocr.DdddOcr(old=True)
    log = GetLogger().get_logger()
    count = 0

    def post(self, _path, _data, **kwargs):
        self.count = self.count + 1
        url = "http://" + lipaiapi.key.ip + _path
        if _data:
            data = json.dumps(_data)
            resp = requests.post(url=url, headers=lipaiapi.key.headers, data=data, **kwargs)
            self.log.info("正在测试本组合用例中的第{}个接口: {}".format(self.count, url))
            self.log.info("传的参数是：{}".format(data))
            self.log.info("接口返回的响应内容中的code是： {}".format(resp.json()["code"]))
            # self.log.info("内容为：{}".format(resp.text))
            try:
                assert resp.json()["code"] == 200, "出现异常，code:{}不等于200".format(resp.json()["code"])
                return resp
            except Exception as e:
                self.log.error(e)
            raise

    def create(self, _data):
        resp = self.post(lipaiapi.key.create_path, _data)
        if resp.json()["code"] == 200:
            self.log.info("新建：创建模型：{}新记录，id为：{}".format(_data["model"], resp.json()["data"]))
        return resp

    def read(self, _data):
        resp = self.post(lipaiapi.key.read_path, _data)
        if resp.json()["code"] == 200:
            self.log.info("查看：查看模型{}中id为：{}的内容： {}".format(_data["model"], _data["id"], resp.json()["data"]))
        return resp

    def edit(self, _data):
        resp = self.post(lipaiapi.key.edit_path, _data)
        if resp.json()["code"] == 200:
            self.log.info("编辑：编辑模型{}中id为：{}的记录已成功".format(_data["model"], _data["id"]))
        return resp

    def delete(self, _data):
        resp = self.post(lipaiapi.key.delete_path, _data)
        if resp.json()["code"] == 200:
            if len(_data["ids"]) == 1:
                self.log.info("删除：已删除模型{}中id为：{}的记录".format(_data["model"], re.findall("\d+", str(_data["ids"]))[0]))
            else:
                self.log.info(
                    "批量删除：已批量删除模型{}中id为：{}的记录".format(_data["model"], str(_data["ids"]).split("[")[1].split("]")[0]))

        return resp

    def pinyin(self, _data):
        resp = self.post(lipaiapi.key.onchange_path, _data)
        return resp

    def name_get(self, _model, _id):
        data = {"model": _model,
                "id": _id}
        resp = self.post(lipaiapi.key.name_get_path, data)
        return resp

    def load_views(self, _data):
        resp = self.post(lipaiapi.key.load_views_path, _data)
        return resp

    def default_get(self, _data):
        resp = self.post(lipaiapi.key.default_get_path, _data)
        if resp.json()["code"] == 200:
            self.log.info("模型：{}的默认填充字段信息为：{}".format(_data["model"], resp.json()["data"]))
        return resp

    def search_read(self, _data):
        resp = self.post(lipaiapi.key.search_read_path, _data)
        if resp.json()["code"] == 200:
            self.log.info("快捷搜索：模型：{}快捷搜索条件按{}搜索{}符合的记录数是：{}条".format(_data["model"],
                                                                 str(_data["domain"]).split(",")[0].split("[")[2],
                                                                 str(_data["domain"]).split(",")[2].split("]")[0],
                                                                 resp.json()["data"]["length"]))
        return resp

    def read_group(self, _data):
        resp = self.post(lipaiapi.key.read_group_path, _data)
        if resp.json()["code"] == 200:
            self.log.info(
                "分组：模型：{}按{}分组，响应内容中的data为：{}".format(_data["model"], str(_data["group"]).split("[")[1].split("]")[0],
                                                      resp.json()["data"]))
        return resp

    def call_method(self, _data, _id):
        resp = self.post(lipaiapi.key.call_method_path, _data)
        if resp.json()["code"] == 200:
            if _data["method"] == "unfreezeButton":
                self.log.info("解冻：已成功解冻模型{}中id为：{}的记录".format(_data["model"], _id))
            elif _data["method"] == "freezeButton":
                self.log.info("冻结：已成功冻结模型{}中id为：{}的记录".format(_data["model"], _id))
            elif _data["method"] == "unAllowMoreChargeButton":
                self.log.info("关闭多充：已成功关闭模型{}中id为：{}的多充功能".format(_data["model"], _id))
            elif _data["method"] == "allowMoreChargeButton":
                self.log.info("打开多充：已成功开启模型{}中id为：{}的多充功能".format(_data["model"], _id))
            # self.log.info("{}：已成功{}模型{}中id为：{}的记录".format(_data["method"], _data["method"], _data["model"], _id))
        return resp

    def login(self):
        url = "http://" + lipaiapi.key.ip + lipaiapi.key.image_path
        resp = requests.get(url=url, headers=lipaiapi.key.headers)
        self.log.info("正在测试前置获取登录验证码接口: {}".format(url))
        self.log.info("接口返回的响应头中的status_code是： {}".format(resp.status_code))
        # 获取到验证码照片的 bytes类型,然后解码
        image = resp.content
        code = self.ocr.classification(image)
        jsessionid = resp.cookies.get_dict()["JSESSIONID"]
        dict1 = {"cookie": "JSESSIONID=" + jsessionid}
        lipaiapi.key.headers = update_dict(dict1, lipaiapi.key.headers)
        data = {"loginCode": "admin", "plantPassword": "12345qwert", "imageCode": code}
        resp = self.post(lipaiapi.key.login_path, data)
        self.log.info("请求登录的响应返回内容是：{}".format(resp.text))
        dict2 = {"Authorization": resp.json()["data"]}
        lipaiapi.key.headers = update_dict(lipaiapi.key.headers, dict2)




