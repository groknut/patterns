from abc import ABC, abstractmethod

from Src.Dtos.filter_dto import filter_dto


class abstract_filter_prototype(ABC):
    """Прототип фильтрации доменных объектов по DTO."""

    @abstractmethod
    def filter(self, objects: list, dto: filter_dto) -> list:
        """Вернуть подмножество objects, удовлетворяющее dto."""
        ...
