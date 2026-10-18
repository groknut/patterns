from Src.Core.abstract_model import abstract_model
from Src.Dtos.report_type_dto import report_type_enum
from Src.Models.company_model import company_model
from Src.Core.validator import validator


class settings_model(abstract_model):
    """Менеджер настроек
    - Организация
    - Руководитель
    - Бухгалтер
    - Первая инициализация (true | false)
    """

    __organization: company_model = None
    __boss_name: str = ""
    __account_name: str = ""
    __is_first_work: bool = False
    __response_format: report_type_enum = report_type_enum.TXT

    @property
    def organization(self) -> company_model:
        """Организация"""
        return self.__organization

    @organization.setter
    def organization(self, value: company_model):
        """Установить значение организации"""
        validator.validate(value, company_model)
        self.__organization = value

    @property
    def boss_name(self) -> str:
        """Имя руководителя"""
        return self.__boss_name

    @boss_name.setter
    def boss_name(self, value: str):
        """Установить имя руководителя"""
        validator.validate(value, str, 255)
        self.__boss_name = value

    @property
    def account_name(self) -> str:
        """Имя бухгалтера"""
        return self.__account_name

    @account_name.setter
    def account_name(self, value: str):
        """Установить имя бухгалтера"""
        validator.validate(value, str, 255)
        self.__account_name = value

    @property
    def is_first(self) -> bool:
        """Первая ли инициализация"""
        return self.__is_first_work

    @is_first.setter
    def is_first(self, value: bool):
        """Установить, первая ли это инициализация"""
        self.__is_first_work = value

    @property
    def response_format(self) -> report_type_enum:
        """Формат вывода отчета по умолчанию (CSV | Markdown | XML | TXT | HTML)"""
        return self.__response_format

    @response_format.setter
    def response_format(self, value) -> None:
        """Устанавливает формат вывода."""
        if isinstance(value, str):
            value = report_type_enum.from_str(value)
        validator.validate(value, report_type_enum)
        self.__response_format = value
