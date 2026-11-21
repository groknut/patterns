

from dataclasses import dataclass

from Src.Core.validator import validator
from Src.Dtos.filter_condition_enum import filter_condition_enum


@dataclass
class filter_dto:
    """DTO для фильтрации данных
    Содержит определения:
        - поле
        - значение
        - условие
    """
    field: str
    value: str
    condition: filter_condition_enum

    def __init__(
        self,
        field: str = "",
        value: str = "",
        condition: filter_condition_enum = filter_condition_enum.EQUALS,
    ) -> None:
        self.field = field
        self.value = value
        self.condition = condition


    @property
    def field(self) -> str:
        return self.__field

    @field.setter
    def field(self, value: str) -> None:
        validator.validate(value, str, 255)
        self.__field = value.strip()

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        validator.validate(value, str, 255)
        self.__value = value

    @property
    def condition(self) -> filter_condition_enum:
        return self.__condition

    @condition.setter
    def condition(self, value) -> None:
        if isinstance(value, str):
            value = filter_condition_enum.from_str(value)
        validator.validate(value, filter_condition_enum)
        self.__condition = value
