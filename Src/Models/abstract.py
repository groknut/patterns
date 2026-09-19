from abc import ABC, abstractmethod
import uuid

class entity(ABC):
    """Класс сущности"""
    @abstractmethod
    def __init__(self):
        """Конструктор для инициализации"""
        """Происходит генерация id"""
        self.__id = uuid.uuid4()
        self.__name = ""

    @abstractmethod
    def set_name(self, name: str):
        """Установка некоторого значения в приватное поле __name"""
        if name == '' or name is None:
            raise ValueError("Имя должно быть заполнено")
        self.__name = name

    @abstractmethod
    @property
    def name(self):
        """Get метод для получения значения __name формата property: Entity.name"""
        return self.__name

    @abstractmethod
    @property
    def id(self):
        """Get метод для получения значения __id формата property: Entity.id"""
        return self.__id
