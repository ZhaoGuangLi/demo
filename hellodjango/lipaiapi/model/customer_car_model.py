import lipaiapi.model
from lipaiapi.key.key import Key
from lipaiapi.model.customer_car_brand import CustomerCarBrand
from lipaiapi.utility.common import dict_key, update_dict
from lipaiapi.model.model_setting import ModelSetting


class CustomerCarModel(Key):
    customer_car_brand = CustomerCarBrand()
    setting = ModelSetting()
    fields = ""
    customer_car_model_id = ""
    carModelId_displayName = ""
    ids_list = []

    def create_customer_car_model(self, create_name):
        self.carModelId_displayName = create_name
        dict1 = self.customer_car_model_default_get()
        dict2 = {"pictureUrl": "https://test3.gcevc.net/oss/customer_car_model/pictureUrl/1651041717176.png",
                 "carBrandId": self.customer_car_brand.customer_car_brand_name(), "name": create_name}
        data = {"model": self.setting.load_data["resModel"],
                "map": update_dict(dict1, dict2)}
        resp = self.create(data)
        self.customer_car_model_id = resp.json()["data"]
        self.ids_list.append(resp.json()["data"])

    def edit_customer_car_model(self, edit_name):
        data = {"model": self.setting.load_data["resModel"], "map": {"name": edit_name},
                "id": self.customer_car_model_id}
        resp = self.edit(data)

    def delete_customer_car_model(self, *args):
        data = {"model": self.setting.load_data["resModel"],
                "ids": [*args]}
        resp = self.delete(data)

    def customer_car_model_fields(self, call_name):
        self.setting.get_fields(call_name)
        return self.setting.fields

    def read_customer_car_model(self):
        data = {"model": self.setting.load_data["resModel"],
                "fields": self.fields,
                "id": self.customer_car_model_id}
        resp = self.read(data)

    def customer_car_model_default_get(self):
        data = {"model": self.setting.load_data["resModel"], "fields": self.fields, "context": {}}
        resp = self.default_get(data)
        return resp.json()["data"]

    def customer_car_model_name(self):
        resp = self.name_get(self.setting.load_data["resModel"], self.customer_car_model_id)
        return resp.json()["data"]

    def customer_car_model_search_read(self, condition, *args):
        dict2 = {"model": self.setting.load_data["resModel"], "fields": self.fields,
                 "domain": [[condition, "like", *args]]}
        data = update_dict(lipaiapi.model.search_read_dict, dict2)
        resp = self.search_read(data)

    def customer_car_brand_read_group(self, condition):
        dict2 = {"model": self.setting.load_data["resModel"], "domain": [],
                 "fields": self.fields,  "group": [condition]}
        data = update_dict(lipaiapi.model.read_group_dict, dict2)
        resp = self.read_group(data)

    def customer_car_model_process(self, call_name, customer_car_brand_name, create_name, edit_name):
        self.customer_car_brand.create_customer_car_brand(customer_car_brand_name)
        self.fields = self.customer_car_model_fields(call_name)
        self.create_customer_car_model(create_name)
        self.read_customer_car_model()
        self.edit_customer_car_model(edit_name)
        self.customer_car_model_search_read("name", edit_name)
        self.customer_car_model_search_read("carBrandId.displayName", self.customer_car_brand.carBrandId_displayName)
        self.customer_car_brand_read_group("carBrandId")
        self.delete_customer_car_model(self.customer_car_model_id)
        self.create_customer_car_model(create_name)
        self.create_customer_car_model(edit_name)
        self.delete_customer_car_model(self.ids_list[1], self.ids_list[2])
        self.customer_car_brand.delete_customer_car_brand(self.customer_car_brand.customer_car_brand_id)

    def create_customer_car_model_process(self, customer_brand_name, customer_model_name):
        self.customer_car_brand.create_customer_car_brand(customer_brand_name)
        self.fields = self.customer_car_model_fields(["????????????", "??????"])
        self.create_customer_car_model(customer_model_name)

    def delete_customer_car_model_process(self):
        self.delete_customer_car_model(self.customer_car_model_id)
        self.customer_car_brand.delete_customer_car_brand(self.customer_car_brand.customer_car_brand_id)


if __name__ == '__main__':
    carBrandId_displayName = "?????????"
    _create_name = "???EV"
    _edit_name = "???EV?????????"
    a = CustomerCarModel()
    a.login()
    a.customer_car_model_process(carBrandId_displayName, _create_name, _edit_name)

