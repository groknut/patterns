

from dataclasses import dataclass
from enum import Enum
from multiprocessing import Condition


class filter_condition_enum(Enum):
    """Условие фильтрации"""
    EQUALS = "EQUALS"
    LIKE = "LIKE"

    @classmethod
    def from_str(cls, value) -> "filter_condition_enum":
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().upper()
        for member in cls:
            if member.value.upper() == normalized:
                return member
        raise ValueError(f"Неизвестное условие фильтрации: {value}")

@dataclass
class filter_dto:
    """DTO для фильтрации данных
    Содержит определения:
        - поле
        - значение
        - условие
    """
    field: str
    value: str
    condition: filter_condition_enum
