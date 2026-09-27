from abc import ABC, abstractmethod
import uuid
from Src.Core.exception import arguments_exception

class abstract_model(ABC):
    """Абстрактный класс доменных моделей
    Содержит только генерацию уникального кода
    """

    def __init__(self) -> None:
        """Конструктор для инициализации. Генерирует id"""
        self.__id = uuid.uuid4().hex
    @property
    def id(self):
        """Get метод для получения значения __id формата property: Entity.id"""
        return self.__id

    @id.setter
    def id(self, v: str) -> None:
        if value is None:
            raise arguments_exception(
                field=value,
                message="Empty id"
            )
        self.__id = value
