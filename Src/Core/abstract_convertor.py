from abc import ABC, abstractmethod
from typing import Any


class abstract_convertor(ABC):
    """Конвертор объекта в словарь {имя_поля: значение}"""

    @property
    @abstractmethod
    def types(self) -> tuple[type, ...]:
        """Кортеж типов, которые поддерживает данный конвертер"""
        ...

    @abstractmethod
    def convert(self, object: Any)->dict:
        """Вернуть словарь по объекту или его полям."""
        ...

    def _find_convertor(
        self, obj: Any, convertors: list["abstract_convertor"]
    ) -> "abstract_convertor | None":
        """Вспомогательный метод для поиска подходящего конвертора."""
        for convertor in convertors:
            if isinstance(obj, convertor.types):
                return convertor
        return None
