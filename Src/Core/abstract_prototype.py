from abc import ABC, abstractmethod
from typing import Any

from Src.Dtos.filter_dto import filter_dto


class abstract_prototype(ABC):
    """Протоитип создаёт новые объекты копированием себя
    Ключевой метод — `clone()`, возвращает НОВЫЙ экземпляр того же класса.
    """

    @abstractmethod
    def clone(self) -> "abstract_prototype":
        """Вернуть копию прототипа (того же типа)."""
        ...
