import lipaiapi.model
from lipaiapi.key.key import Key
from lipaiapi.utility.common import dict_key, update_dict
from lipaiapi.model.model_setting import ModelSetting


class CustomerCarBrand(Key):
    customer_car_brand_id = ""
    carBrandId_displayName = ""
    setting = ModelSetting()
    fields = ""
    ids_list = []

    def create_customer_car_brand(self, create_name):
        self.carBrandId_displayName = create_name
        data = {"model": self.setting.load_data["resModel"],
                "map": {"logoUrl": "https://test3.gcevc.net/oss/customer_car_brand/logoUrl/1651026599188.png",
                        "name": create_name, "pinyin": self.get_pinyin(create_name)}}
        resp = self.create(data)
        self.customer_car_brand_id = resp.json()["data"]
        self.ids_list.append(resp.json()["data"])

    def get_pinyin(self, _name):
        data = {"id": self.customer_car_brand_id, "model": self.setting.load_data["resModel"], "field": "name",
                "map": {"name": _name},
                "method": "pinyinOnchange"}
        resp = self.pinyin(data)
        pinyin = resp.json()["data"]["value"]["pinyin"]
        return pinyin

    def edit_customer_car_brand(self, edit_name):
        data = {"model": self.setting.load_data["resModel"],
                "map": {"name": edit_name, "pinyin": self.get_pinyin(edit_name)}, "id": self.customer_car_brand_id}
        resp = self.edit(data)

    def delete_customer_car_brand(self, *args):
        data = {"model": self.setting.load_data["resModel"],
                "ids": [*args]}
        resp = self.delete(data)

    def customer_car_brand_name(self):
        resp = self.name_get(self.setting.load_data["resModel"], self.customer_car_brand_id)
        return resp.json()["data"]

    def customer_car_brand_fields(self, call_name):
        self.setting.get_fields(call_name)
        return self.setting.fields

    def read_customer_car_brand(self, _id):
        data = {"model": self.setting.load_data["resModel"],
                "fields": self.fields,
                "id": _id}
        resp = self.read(data)

    def customer_car_brand_search_read(self, condition, *args):
        """
        快捷搜索
        :param condition: 条件
        :param args: 搜索输入的内容
        :return: 无
        """
        dict2 = {"model": self.setting.load_data["resModel"], "fields": self.fields,
                 "domain": [[condition, "ilike", *args]]}
        data = update_dict(lipaiapi.model.search_read_dict, dict2)
        resp = self.search_read(data)

    def customer_car_brand_process(self, call_name, create_name, edit_name):
        self.fields = self.customer_car_brand_fields(call_name)
        self.create_customer_car_brand(create_name)
        self.read_customer_car_brand(self.customer_car_brand_id)
        self.edit_customer_car_brand(edit_name)
        self.customer_car_brand_search_read("name", edit_name)
        self.delete_customer_car_brand(self.customer_car_brand_id)
        self.create_customer_car_brand(create_name)
        self.create_customer_car_brand(edit_name)
        self.delete_customer_car_brand(self.ids_list[1], self.ids_list[2])


if __name__ == '__main__':
    name1 = "比亚迪"
    name2 = "比亚迪汉"
    a = CustomerCarBrand()
    a.login()
    a.customer_car_brand_process(name1, name2)
