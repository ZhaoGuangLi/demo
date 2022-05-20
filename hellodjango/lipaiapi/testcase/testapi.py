import os
import re
import pytest
import allure
from lipaiapi.utility.read_json import read_json
from lipaiapi.model.model_object import ModelObject
from lipaiapi.model.model_setting import ModelSetting


class TestApi:
    login = ModelSetting()
    object = ModelObject()

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("登录模块-登录（获取验证码-登录-查看登录用户信息）")
    @allure.title("登录模块-登录（获取验证码-登录-查看登录用户信息）")
    @pytest.mark.parametrize("case_info", read_json("user.json"))
    @pytest.mark.run(order=0.5)
    def test_login(self, case_info):
        self.login.login_process(case_info["username"], case_info["password"])

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("车辆品牌模块-汽车品牌（增-查-改-快捷搜索-删-新增（两个）-批量删除）")
    @allure.title("车辆品牌模块-汽车品牌（增-查-改-按汽车name快捷搜索-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("customer_car_brand.json"))
    @pytest.mark.run(order=1)
    def test_customer_car_brand(self, case_info):
        customer_car_brand = self.object.get_customer_car_brand_object()
        customer_car_brand.customer_car_brand_process(case_info["模块"], case_info["create_name"], case_info["edit_name"])

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("车型模块-车型（增-查-改-按(车型name,汽车品牌name快捷搜索-按汽车品牌分组-删-新增（两个）-批量删除）")
    @allure.title("车型模块-车型（增-查-改-按(车型name,汽车品牌name）快捷搜索-按汽车品牌分组-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("customer_car_model.json"))
    @pytest.mark.run(order=2)
    def test_customer_car_model(self, case_info):
        customer_car_model = self.object.get_customer_car_model_object()
        customer_car_model.customer_car_model_process(case_info["模块"], case_info["customer_car_brand_name"],
                                                      case_info["create_name"], case_info["edit_name"])

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("车辆模块-汽车（增-查-改-按(车牌号,自编号，车架号，车型名，客户名）快捷搜索-按（客户，车型）分组-删-新增（两个）-批量删除）")
    @allure.title("车辆模块-汽车（增-查-改-按(车牌号,自编号，车架号，车型名，客户名）快捷搜索-按（客户，车型）分组-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("customer_car.json"))
    @pytest.mark.run(order=3)
    def test_customer_car(self, case_info):
        customer_car = self.object.get_customer_car_object()
        customer_car.customer_car_process(case_info["模块"], case_info["customer_car_brand_name"],
                                          case_info["customer_car_model_name"], case_info["create_number"],
                                          case_info["create_remark"], case_info["create_vin"], case_info["edit_number"],
                                          case_info["edit_remark"], case_info["edit_vin"])

    @allure.severity("critical")
    @allure.tag("立牌快充自动化接口测试")
    @allure.description("充电卡模块-充电卡（增-查-改-按(名称,充电卡号，序号，客户名）快捷搜索-按（客户，允许多充）分组-删-新增（两个）-批量删除）")
    @allure.title("充电卡模块-充电卡（增-查-改-按(名称,充电卡号，序号，客户名）快捷搜索-按（客户，允许多充）分组-删-新增（两个）-批量删除）")
    @pytest.mark.parametrize("case_info", read_json("customer_card.json"))
    @pytest.mark.run(order=4)
    def test_customer_card(self, case_info):
        customer_card = self.object.get_customer_card_object()
        customer_card.customer_card_process(case_info["模块"], case_info["create_card_number"], case_info["create_name"],
                                            case_info["create_code"], case_info["edit_card_number"],
                                            case_info["edit_name"], case_info["edit_code"])
    #
    # @allure.severity("critical")
    # @allure.tag("立牌快充自动化接口测试")
    # @allure.description("个人客户模块-个人客户（增-查-改-按(姓名，电话号码）快捷搜索-按（性别，状态））分组-冻结-解冻-允许多充-不允许多充")
    # @allure.title("个人客户模块-个人客户（增-查-改-按(姓名，电话号码）快捷搜索-按（性别，状态）分组-冻结-解冻-允许多充-不允许多充")
    # @pytest.mark.run(order=5)
    # def test_customer(self):
    #     customer = self.object.get_customer_object()
    #     customer.customer_process(["客户管理", "个人客户"])
    #
    # @allure.severity("critical")
    # @allure.tag("立牌快充自动化接口测试")
    # @allure.description("公司客户模块-公司客户（增-查-改-按(姓名，电话号码）快捷搜索-按（性别，状态））分组-冻结-解冻-允许多充-不允许多充")
    # @allure.title("公司客户模块-公司客户（增-查-改-按(姓名，电话号码）快捷搜索-按状态分组-冻结-解冻-允许多充-不允许多充")
    # @pytest.mark.run(order=6)
    # def test_company_customer(self):
    #     company_customer = self.object.get_company_customer_object()
    #     company_customer.company_customer_process(["客户管理", "公司客户"])


if __name__ == '__main__':
    pytest.main(['./lipaiapi/testcase/testapi.py', '-vs', '--alluredir=./lipaiapi/temp', '--clean-alluredir'])
    # os.system("allure serve ./lipaiapi/temp -p 8003")


