import lipaiapi.model
from lipaiapi.key.key import Key
from lipaiapi.model.customer_car_model import CustomerCarModel
from lipaiapi.utility.common import dict_key, update_dict


class CustomerCar(Key):
    customer_car_model = CustomerCarModel()
    customer_car_id = ""
    customer = "zhao_test"
    ids_list = []

    def create_customer_car(self, create_number, create_remark, create_vin):
        dict1 = self.customer_car_default_get()
        dict2 = {"carModelId": self.customer_car_model.customer_car_model_name(), "customerId": {},
                 "number": create_number, "remark": create_remark, "vin": create_vin,
                 "pictureUrl": "https://test3.gcevc.net/oss/customer_car/pictureUrl/1651051712594.png"}
        data = {"model": lipaiapi.model.model_customer_car,
                "map": update_dict(dict1, dict2)}
        resp = self.create(data)
        self.customer_car_id = resp.json()["data"]
        self.ids_list.append(resp.json()["data"])

    def edit_customer_car(self, edit_number, edit_remark, edit_vin):
        data = {"model": lipaiapi.model.model_customer_car,
                "map": {"number": edit_number, "remark": edit_remark, "vin": edit_vin}, "id": self.customer_car_id}
        resp = self.edit(data)

    def delete_customer_car(self, *args):
        data = {"model": lipaiapi.model.model_customer_car,
                "ids": [*args]}
        resp = self.delete(data)

    def customer_car_fields(self):
        data = {"model": lipaiapi.model.base_view_model, "resModel": lipaiapi.model.model_customer_car,
                "kwargs": {"context": {"lang": "zh_CN"}, "views": [[False, "tree"], [False, "form"], [False, "search"]]}}
        resp = self.load_views(data)
        fields_dict = resp.json()["data"]["fields"]
        fields = dict_key(fields_dict)
        return fields

    def read_customer_car(self):
        data = {"model": lipaiapi.model.model_customer_car,
                "fields": self.customer_car_fields(),
                "id": self.customer_car_id}
        resp = self.read(data)

    def customer_car_default_get(self):
        data = {"model": lipaiapi.model.model_customer_car, "fields": self.customer_car_fields(), "context": {}}
        resp = self.default_get(data)
        return resp.json()["data"]

    def customer_car_search_read(self, condition, *args):
        dict2 = {"model": lipaiapi.model.model_customer_car, "fields": self.customer_car_fields(),
                 "domain": [[condition, "like", *args]]}
        data = update_dict(lipaiapi.model.search_read_dict, dict2)
        resp = self.search_read(data)

    def customer_car_read_group(self, condition):
        dict2 = {"model": lipaiapi.model.model_customer_car, "domain": [],
                 "fields": self.customer_car_fields(),  "group": [condition]}
        data = update_dict(lipaiapi.model.read_group_dict, dict2)
        resp = self.read_group(data)

    def customer_car_process(self, customer_brand_name, customer_model_name, create_number, create_remark, create_vin,
                             edit_number, edit_remark, edit_vin):
        self.customer_car_model.create_customer_car_model_process(customer_brand_name, customer_model_name)
        self.create_customer_car(create_number, create_remark, create_vin)
        self.read_customer_car()
        self.edit_customer_car(edit_number, edit_remark, edit_vin)
        self.customer_car_search_read("number", edit_number)
        self.customer_car_search_read("remark", edit_remark)
        self.customer_car_search_read("vin", edit_vin)
        self.customer_car_search_read("carModelId.displayName", self.customer_car_model.carModelId_displayName)
        self.customer_car_search_read("customerId.displayName", self.customer)
        self.customer_car_read_group("customerId")
        self.customer_car_read_group("carModelId")
        self.delete_customer_car(self.customer_car_id)
        self.create_customer_car(create_number, create_remark, create_vin)
        self.create_customer_car(edit_number, edit_remark, edit_vin)
        self.delete_customer_car(self.ids_list[1], self.ids_list[2])
        self.customer_car_model.delete_customer_car_model_process()

    def create_customer_car_process(self, customer_brand_name, customer_model_name, create_number, create_remark,
                                    create_vin):
        self.customer_car_model.create_customer_car_model_process(customer_brand_name, customer_model_name)
        self.create_customer_car(create_number, create_remark, create_vin)

    def delete_customer_car_process(self):
        self.delete_customer_car(self.customer_car_id)
        self.customer_car_model.delete_customer_car_model_process()


if __name__ == '__main__':
    _customer_brand_name = "比亚迪"
    _customer_model_name = "汉EV"
    _create_number = "粤GF520U"
    _create_remark = "粤GF520U"
    _create_vin = "TEST0000000000002"
    _edit_number = "粤GF920U"
    _edit_remark = "粤GF920U"
    _edit_vin = "TEST0000000000005"
    a = CustomerCar()
    a.login()
    a.customer_car_process(_customer_brand_name, _customer_model_name, _create_number, _create_remark, _create_vin,
                           _edit_number, _edit_remark, _edit_vin)
