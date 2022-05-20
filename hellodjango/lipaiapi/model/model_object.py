from lipaiapi.model.customer_card import CustomerCard
from lipaiapi.model.customer_car import CustomerCar
from lipaiapi.model.company_customer_info import CompanyCustomerInfo
from lipaiapi.model.customer_car_brand import CustomerCarBrand
from lipaiapi.model.customer_car_model import CustomerCarModel
from lipaiapi.model.customer_info import CustomerInfo


class ModelObject:
    @classmethod
    def get_customer_object(cls):
        return CustomerInfo()

    @classmethod
    def get_company_customer_object(cls):
        return CompanyCustomerInfo()

    @classmethod
    def get_customer_car_brand_object(cls):
        return CustomerCarBrand()

    @classmethod
    def get_customer_car_model_object(cls):
        return CustomerCarModel()

    @classmethod
    def get_customer_car_object(cls):
        return CustomerCar()

    @classmethod
    def get_customer_card_object(cls):
        return CustomerCard()
