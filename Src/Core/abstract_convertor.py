from abc import ABC, abstractmethod
from typing import Any


class abstract_convertor(ABC):
    """Конвертор объекта в словарь {имя_поля: значение}"""
    @abstractmethod
    def convert(self, object: Any)->dict:
        """Вернуть словарь по объекту или его полям."""
        ...
