from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator


class entity_model(abstract_model):
    """Общий класс для наследования доменных моделей
    Содержит определения:
        - уникальный код
        - наименование
    """

    __name: str = ""
    __max_length: int = 50

    @property
    def name(self) -> str:
        """Возвращает наименование"""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Установка наименования сущности"""
        validator.validate(value, str, self.__max_length)
        self.__name = value.strip()

    @property
    def max_length(self) -> int:
        """Возвращает максимально допустимую длину наименвоания"""
        return self.__max_length
