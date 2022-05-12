import random
import lipaiapi.model
from lipaiapi.key.key import Key
from lipaiapi.utility.common import dict_key, update_dict, generate_customer_name, generate_phone_number


class CustomerInfo(Key):
    customer_info_id = ""
    customerId_displayName = ""
    customerId_phone = ""
    button_list = ["freezeButton", "unfreezeButton", "allowMoreChargeButton", "unAllowMoreChargeButton"]

    def create_customer_info(self):
        self.customerId_displayName = generate_customer_name()
        self.customerId_phone = generate_phone_number()
        dict1 = self.customer_info_default_get()
        dict2 = {"name": self.customerId_displayName, "phone": self.customerId_phone, "sex": random.randint(0, 2)}
        data = {"model": lipaiapi.model.customer_info_model, "map": update_dict(dict1, dict2)}
        resp = self.create(data)
        self.customer_info_id = resp.json()["data"]

    def edit_customer_info(self):
        self.customerId_displayName = generate_customer_name()
        self.customerId_phone = generate_phone_number()
        data = {"model": lipaiapi.model.customer_info_model,
                "map": {"name": self.customerId_displayName, "phone": self.customerId_phone},
                "id": self.customer_info_id}
        resp = self.edit(data)

    def customer_info_name(self, customer_id):
        """
        新建其他记录选择客户时所需的字段信息
        :param customer_id:客户Id
        :return:创建框选择客户时所需的字段
        """
        resp = self.name_get(lipaiapi.model.customer_info_model, customer_id)
        return resp.json()["data"]

    def customer_info_fields(self):
        data = {"model": lipaiapi.model.base_view_model, "resModel": lipaiapi.model.customer_info_model,
                "kwargs": {"context": {"lang": "zh_CN"}, "views": [[97, "tree"], [98, "form"], [99, "search"]]}}
        resp = self.load_views(data)
        fields_dict = resp.json()["data"]["fields"]
        fields = dict_key(fields_dict)
        return fields

    def read_customer_info(self, _id):
        data = {"model": lipaiapi.model.customer_info_model,
                "fields": self.customer_info_fields(),
                "id": _id}
        resp = self.read(data)

    def customer_info_search_read(self, condition, *args):
        dict2 = {"model": lipaiapi.model.customer_info_model, "fields": self.customer_info_fields(),
                 "domain": [[condition, "ilike", *args]]}
        data = update_dict(lipaiapi.model.search_read_dict, dict2)
        resp = self.search_read(data)

    def customer_info_default_get(self):
        data = {"model": lipaiapi.model.customer_info_model,
                "fields": self.customer_info_fields(), "context": {"default_type": 0}}
        resp = self.default_get(data)
        return resp.json()["data"]

    def customer_info_read_group(self, condition):
        dict2 = {"model": lipaiapi.model.customer_info_model, "domain": [],
                 "fields": self.customer_info_fields(),  "group": [condition]}
        data = update_dict(lipaiapi.model.read_group_dict, dict2)
        resp = self.read_group(data)

    def customer_info_call_method(self, button):
        data = {"model": lipaiapi.model.customer_info_model, "method": button,
                "args": [[self.customer_info_id], {}]}
        resp = self.call_method(data, self.customer_info_id)

    def customer_process(self):
        self.create_customer_info()
        self.read_customer_info(self.customer_info_id)
        self.edit_customer_info()
        self.customer_info_search_read("name", self.customerId_displayName)
        self.customer_info_search_read("phone", self.customerId_phone)
        self.customer_info_read_group("sex")
        self.customer_info_read_group("status")
        for i in range(len(self.button_list)):
            self.customer_info_call_method(self.button_list[i])


if __name__ == '__main__':
    a = CustomerInfo()

