from Src.Core.abstract_model import abstract_model
from Src.Models.company_model import company_model
from Src.Core.validator import validator

class settings_model(abstract_model):
    __organization: company_model = None
    __boss_name: str = ''
    __account_name: str = ''
    __is_first_work: bool = False

    @property
    def organization(self) -> company_model:
        return self.__organization

    @organization.setter
    def organization(self, value: company_model):
        validator.validate(value, company_model)
        self.__organization = value

    @property
    def boss_name(self) -> str:
        return self.__boss_name

    @boss_name.setter
    def boss_name(self, value: str):
        validator.validate(value, str, 255)
        self.__boss_name = value

    @property
    def account_name(self) -> str:
        return self.__account_name

    @boss_name.setter
    def account_name(self, value: str):
        validator.validate(value, str, 255)
        self.__account_name = value

    @property
    def is_first(self) -> bool:
        return self.__is_first_work

    @is_first.setter
    def is_first(self, value: bool):
        self.__is_first_work = value
