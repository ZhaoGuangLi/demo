import os
import re

import pytest
import allure
from lipaiapi.model.customer_car import CustomerCar
from lipaiapi.model.customer_car_brand import CustomerCarBrand
from lipaiapi.model.customer_car_model import CustomerCarModel
from lipaiapi.model.customer_card import CustomerCard
from lipaiapi.utility.read_json import read_json
from lipaiapi.model.company_customer_info import CompanyCustomerInfo
from lipaiapi.model.customer_info import CustomerInfo


class TestApi:
    customer_car_brand = CustomerCarBrand()
    customer_car_model = CustomerCarModel()
    customer_car = CustomerCar()
    customer_card = CustomerCard()
    customer = CustomerInfo()
    company_customer = CompanyCustomerInfo()

    @classmethod
    def setup_class(cls):
        cls.customer_car_brand.login()

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("汽车品牌模块-汽车品牌（增-查-改-快捷搜索-删-新增（两个）-批量删除）")
    @allure.title("汽车品牌模块-汽车品牌（增-查-改-按汽车name快捷搜索-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("./lipaiapi/testcase/customer_car_brand.json"))
    @pytest.mark.run(order=1)
    def test_customer_car_brand(self, case_info):
        self.customer_car_brand.customer_car_brand_process(case_info["create_name"], case_info["edit_name"])

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("车型模块-车型（增-查-改-按(车型name,汽车品牌name快捷搜索-按汽车品牌分组-删-新增（两个）-批量删除）")
    @allure.title("车型模块-车型（增-查-改-按(车型name,汽车品牌name）快捷搜索-按汽车品牌分组-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("./lipaiapi/testcase/customer_car_model.json"))
    @pytest.mark.run(order=2)
    def test_customer_car_model(self, case_info):
        self.customer_car_model.customer_car_model_process(case_info["customer_car_brand_name"],
                                                           case_info["create_name"], case_info["edit_name"])

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("车辆模块-汽车（增-查-改-按(车牌号,自编号，车架号，车型名，客户名）快捷搜索-按（客户，车型）分组-删-新增（两个）-批量删除）")
    @allure.title("车辆模块-汽车（增-查-改-按(车牌号,自编号，车架号，车型名，客户名）快捷搜索-按（客户，车型）分组-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("./lipaiapi/testcase/customer_car.json"))
    @pytest.mark.run(order=3)
    def test_customer_car(self, case_info):
        self.customer_car.customer_car_process(case_info["customer_car_brand_name"],
                                               case_info["customer_car_model_name"], case_info["create_number"],
                                               case_info["create_remark"], case_info["create_vin"],
                                               case_info["edit_number"], case_info["edit_remark"],
                                               case_info["edit_vin"])

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("充电卡模块-充电卡（增-查-改-按(名称,充电卡号，序号，客户名）快捷搜索-按（客户，允许多充）分组-删-新增（两个）-批量删除）")
    @allure.title("充电卡模块-充电卡（增-查-改-按(名称,充电卡号，序号，客户名）快捷搜索-按（客户，允许多充）分组-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("./lipaiapi/testcase/customer_card.json"))
    @pytest.mark.run(order=4)
    def test_customer_card(self, case_info):
        self.customer_card.customer_card_process(case_info["create_card_number"], case_info["create_name"],
                                                 case_info["create_code"], case_info["edit_card_number"],
                                                 case_info["edit_name"], case_info["edit_code"])
    #
    # @allure.severity("critical")
    # @allure.tag("立牌快充自动化接口测试")
    # @allure.description("个人客户模块-个人客户（增-查-改-按(姓名，电话号码）快捷搜索-按（性别，状态））分组-冻结-解冻-允许多充-不允许多充")
    # @allure.title("个人客户模块-个人客户（增-查-改-按(姓名，电话号码）快捷搜索-按（性别，状态）分组-冻结-解冻-允许多充-不允许多充")
    # @pytest.mark.run(order=5)
    # def test_customer(self):
    #     self.customer.customer_process()
    #
    # @allure.severity("critical")
    # @allure.tag("立牌快充自动化接口测试")
    # @allure.description("公司客户模块-公司客户（增-查-改-按(姓名，电话号码）快捷搜索-按（性别，状态））分组-冻结-解冻-允许多充-不允许多充")
    # @allure.title("公司客户模块-公司客户（增-查-改-按(姓名，电话号码）快捷搜索-按状态分组-冻结-解冻-允许多充-不允许多充")
    # @pytest.mark.run(order=6)
    # def test_company_customer(self):
    #     self.company_customer.company_customer_process()


if __name__ == '__main__':
    pytest.main(['./lipaiapi/testcase/testapi.py', '-vs', '--alluredir=./lipaiapi/temp', '--clean-alluredir'])
    # os.system("allure serve ./lipaiapi/temp -p 8003")


