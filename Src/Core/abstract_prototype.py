from abc import ABC, abstractmethod
from typing import Any

from Src.Dtos.filter_dto import filter_dto


class abstract_prototype(ABC):
    """Прототип обработки доменных объектов.

    Реализации: filter_prototype (фильтрация), balance_prototype (ОСВ).
    """

    @abstractmethod
    def process(self, source: list, dto: filter_dto | None = None) -> Any:
        """Обработать список объектов. DTO опционально."""
        ...
