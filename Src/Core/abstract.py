from abc import ABC, abstractmethod
import uuid
from Src.Core.exception import arguments_exception

class entity(ABC):
    """Класс сущности"""
    def __init__(self):
        """Конструктор для инициализации. Генерирует id"""
        self.__id = uuid.uuid4().hex
        self.__name = ""

    @property
    # @abstractmethod
    def name(self):
        """Get метод для получения значения __name формата property: Entity.name"""
        return self.__name

    @name.setter
    def name(self, new_name: str):
        """Установка некоторого значения в приватное поле __name"""
        if new_name == '' or new_name is None:
            raise arguments_exception(
                field=new_name,
                message="Empty name"
            )
        self.__name = new_name

    @property
    # @abstractmethod
    def id(self):
        """Get метод для получения значения __id формата property: Entity.id"""
        return self.__id

    @id.setter
    def id(self, new_id: str):
        if new_id is None:
            raise arguments_exception(
                field=new_id,
                message="Empty id"
            )
        self.__id = new_id
