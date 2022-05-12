import lipaiapi.model
from lipaiapi.key.key import Key
from lipaiapi.model.customer_car_brand import CustomerCarBrand
from lipaiapi.utility.common import dict_key, update_dict


class CustomerCard(Key):
    customer_card_id = ""
    cardModelId_displayName = ""
    cardModelId_code = ""
    cardModelId_number = ""
    ids_list = []

    def create_customer_card(self, create_card_number, create_name, create_code):
        self.cardModelId_number = create_card_number
        self.cardModelId_displayName = create_name
        self.cardModelId_code = create_code
        dict1 = self.customer_card_default_get()
        dict2 = {"cardNo": create_card_number, "name": create_name, "code": create_code}
        data = {"model": lipaiapi.model.customer_card_model,
                "map": update_dict(dict1, dict2)}
        resp = self.create(data)
        self.customer_card_id = resp.json()["data"]
        self.ids_list.append(resp.json()["data"])

    def edit_customer_card(self, edit_card_number, edit_name, edit_code):
        self.cardModelId_number = edit_card_number
        self.cardModelId_displayName = edit_name
        self.cardModelId_code = edit_code
        data = {"model": lipaiapi.model.customer_card_model,
                "map": {"cardNo": edit_card_number, "name": edit_name, "code": edit_code},
                "id": self.customer_card_id}
        resp = self.edit(data)

    def delete_customer_card(self, *args):
        data = {"model": lipaiapi.model.customer_card_model,
                "ids": [*args]}
        resp = self.delete(data)

    def customer_card_fields(self):
        data = {"model": lipaiapi.model.base_view_model, "resModel": lipaiapi.model.customer_card_model,
                "kwargs": {"context": {"lang": "zh_CN"},
                           "views": [[False, "tree"], [False, "form"], [False, "search"]]}}
        resp = self.load_views(data)
        fields_dict = resp.json()["data"]["fields"]
        fields = dict_key(fields_dict)
        return fields

    def read_customer_card(self):
        data = {"model": lipaiapi.model.customer_card_model,
                "fields": self.customer_card_fields(),
                "id": self.customer_card_id}
        resp = self.read(data)

    def customer_card_default_get(self):
        data = {"model": lipaiapi.model.customer_card_model, "fields": self.customer_card_fields(), "context": {}}
        resp = self.default_get(data)
        return resp.json()["data"]

    def customer_card_name(self):
        resp = self.name_get(lipaiapi.model.customer_card_model, self.customer_card_id)
        return resp.json()["data"]

    def customer_card_search_read(self, condition, *args):
        dict2 = {"model": lipaiapi.model.customer_card_model, "fields": self.customer_card_fields(),
                 "domain": [[condition, "like", *args]]}
        data = update_dict(lipaiapi.model.search_read_dict, dict2)
        resp = self.search_read(data)

    def customer_car_brand_read_group(self, condition):
        dict2 = {"model": lipaiapi.model.customer_card_model, "domain": [],
                 "fields": self.customer_card_fields(),  "group": [condition]}
        data = update_dict(lipaiapi.model.read_group_dict, dict2)
        resp = self.read_group(data)

    def customer_card_process(self, create_card_number, create_name, create_code, edit_card_number, edit_name,
                              edit_code):
        self.create_customer_card(create_card_number, create_name, create_code)
        self.read_customer_card()
        self.edit_customer_card(edit_card_number, edit_name, edit_code)
        self.customer_card_search_read("name", self.cardModelId_displayName)
        self.customer_card_search_read("cardNo", self.cardModelId_number)
        self.customer_card_search_read("code", self.cardModelId_code)
        self.customer_card_search_read("customerId.displayName", self.cardModelId_code)
        self.customer_car_brand_read_group("customerId")
        self.customer_car_brand_read_group("allowMoreCharge")
        self.delete_customer_card(self.customer_card_id)
        self.create_customer_card(create_card_number, create_name, create_code)
        self.create_customer_card(edit_card_number, edit_name, edit_code)
        self.delete_customer_card(self.ids_list[1], self.ids_list[2])

    def create_customer_card_process(self, customer_brand_name, customer_model_name):
        pass

    def delete_customer_card_process(self):
        pass


if __name__ == '__main__':
    number1 = "1568975633213"
    name1 = "充电卡测试新增"
    code1 = "1568975633213"
    number2 = "7138975633213"
    name2 = "充电卡测试修改"
    code2 = "7138975633213"
    a = CustomerCard()
    a.login()
    a.customer_card_process(number1, name1, code1, number2, name2, code2)

