from abc import ABC, abstractmethod
import uuid
from Src.Core.validator import argument_exception


class abstract_model(ABC):
    """Абстрактный класс доменных моделей
    Содержит только генерацию уникального кода
    """

    def __init__(self) -> None:
        """Конструктор для инициализации. Генерирует id"""
        self.__id = uuid.uuid4().hex

    @property
    def id(self) -> str:
        """Возвращает уникальный код модели"""
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        """Устанавливает уникальный код модели"""
        if value.strip() == "":
            raise argument_exception("value", "Некорректно передан параметр")
        self.__id = value.strip()

    def __eq__(self, value) -> bool:
        if value is None:
            return False
        if not isinstance(value, abstract_model):
            return False
        return self.id == value.id
