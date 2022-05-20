import lipaiapi.model
from lipaiapi.key.key import Key
from lipaiapi.utility.common import update_dict, generate_phone_number, generate_customer_name
from lipaiapi.model.model_setting import ModelSetting


class CompanyCustomerInfo(Key):
    setting = ModelSetting()
    fields = ""
    customer_info_id = ""
    customerId_displayName = ""
    customerId_phone = ""
    button_list = ["freezeButton", "unfreezeButton", "allowMoreChargeButton", "unAllowMoreChargeButton"]
    finance_account_code = ""
    finance_account_id = ""

    def create_customer_info(self):
        self.customerId_displayName = generate_customer_name()
        self.customerId_phone = generate_phone_number()
        dict1 = self.customer_info_default_get()
        dict2 = {"name": self.customerId_displayName, "phone": self.customerId_phone}
        data = {"model": self.setting.load_data["resModel"], "map": update_dict(dict1, dict2)}
        resp = self.create(data)
        self.customer_info_id = resp.json()["data"]

    def edit_customer_info(self):
        self.customerId_displayName = generate_customer_name()
        self.customerId_phone = generate_phone_number()
        data = {"model": self.setting.load_data["resModel"],
                "map": {"name": self.customerId_displayName, "phone": self.customerId_phone},
                "id": self.customer_info_id}
        resp = self.edit(data)

    def customer_info_name(self, customer_id):
        """
        新建其他记录选择客户时所需的字段信息
        :param customer_id:客户Id
        :return:创建框选择客户时所需的字段
        """
        resp = self.name_get(self.setting.load_data["resModel"], customer_id)
        return resp.json()["data"]

    def customer_info_fields(self, call_name):
        self.setting.get_fields(call_name)
        return self.setting.fields

    def read_customer_info(self, _id):
        data = {"model": self.setting.load_data["resModel"],
                "fields": self.fields,
                "id": _id}
        resp = self.read(data)

    def customer_info_search_read(self, condition, *args):
        dict2 = {"model": self.setting.load_data["resModel"], "fields": self.fields,
                 "domain": [[condition, "ilike", *args]]}
        data = update_dict(lipaiapi.model.search_read_dict, dict2)
        resp = self.search_read(data)
        self.finance_account_id = resp.json()["data"]["records"][0]["accountId"]["id"]
        self.finance_account_code = resp.json()["data"]["records"][0]["accountId"]["code"]

    def customer_info_default_get(self):
        data = {"model": self.setting.load_data["resModel"],
                "fields": self.fields, "context": {"default_type": 1}}
        resp = self.default_get(data)
        return resp.json()["data"]

    def customer_info_read_group(self, condition):
        dict2 = {"model": self.setting.load_data["resModel"], "domain": [],
                 "fields": self.fields,  "group": [condition]}
        data = update_dict(lipaiapi.model.read_group_dict, dict2)
        resp = self.read_group(data)

    def customer_info_call_method(self, button):
        data = {"model": self.setting.load_data["resModel"], "method": button,
                "args": [[self.customer_info_id], {}]}
        resp = self.call_method(data, self.customer_info_id)

    def company_customer_process(self, call_name):
        self.fields = self.customer_info_fields(call_name)
        self.create_customer_info()
        self.read_customer_info(self.customer_info_id)
        self.edit_customer_info()
        self.customer_info_search_read("name", self.customerId_displayName)
        print(self.finance_account_code)
        print(self.finance_account_id)
        self.customer_info_search_read("phone", self.customerId_phone)
        self.customer_info_read_group("status")
        for i in range(len(self.button_list)):
            self.customer_info_call_method(self.button_list[i])


if __name__ == '__main__':
    a = CompanyCustomerInfo()
