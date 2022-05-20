import os
import re
import sys
import time
import json
import datetime
import random
import glob
import pickle
import subprocess
import urllib
import shutil
import platform
import ddddocr
import lipaiapi.model
from lipaiapi.key.key import Key
from lipaiapi.utility.common import random_num, dict_key


class ModelSetting(Key):
    call_data = ""
    load_data = ""
    fields = ""
    ocr = ddddocr.DdddOcr(old=True)

    def get_verification_code(self):
        data = {"t": "0.029693380014191195"}
        resp = self.get_image_code(data)
        image = resp.content
        code = self.ocr.classification(image)
        jsessionid = resp.cookies.get_dict()["JSESSIONID"]
        _dict = {"cookie": "JSESSIONID=" + jsessionid}
        self.update_headers(_dict)
        return code

    def user_login(self, username, password):
        data = {"loginCode": username, "plantPassword": password, "imageCode": self.get_verification_code()}
        resp = self.login(data)
        _dict = {"Authorization": resp.json()["data"]}
        self.update_headers(_dict)

    def user_get_info(self):
        data = {"t": random_num()}
        resp = self.get_user_info(data)
        lipaiapi.model.lang = resp.json()["data"]["lang"]

    def model_view_call(self):
        data = {"lang": lipaiapi.model.lang, "t": random_num()}
        resp = self.call(data)
        self.call_data = resp.json()["data"]

    def model_view_load(self, call_name):
        _id = ""
        _model = ""
        for i in self.call_data:
            if call_name[0] == i["name"]:
                for j in i["childIds"]:
                    if call_name[1] == j["name"]:
                        _id = str(j["action"]).split(",")[1]
                        _model = str(j["action"]).split(",")[0]
        data = {"model": _model, "actionId": _id}
        resp = self.load(data, call_name)
        self.load_data = resp.json()["data"]

    def model_view_load_views(self):
        data = {"model": lipaiapi.model.base_view_model, "resModel": self.load_data["resModel"],
                "kwargs": {"context": {"lang": lipaiapi.model.lang}, "views": self.load_data["views"]}}
        resp = self.load_views(data)
        fields_dict = resp.json()["data"]["fields"]
        self.fields = dict_key(fields_dict)

    def get_fields(self, call_name):
        self.model_view_call()
        self.model_view_load(call_name)
        self.model_view_load_views()

    def login_process(self, username, password):
        self.user_login(username, password)
        self.user_get_info()




