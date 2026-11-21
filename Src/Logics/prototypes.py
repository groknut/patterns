from typing import Any

from Src.Core.abstract_prototype import abstract_prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_condition_enum import filter_condition_enum


class filter_prototype(abstract_prototype):
    """Фильтрация доменных объектов.
    Хранит исходный список и «текущий» отфильтрованный. clone() — копия.
    """

    def __init__(self, source: list) -> None:
        self.__source: list = list(source)

    @property
    def data(self) -> list:
        return list(self.__source)

    def clone(self) -> "filter_prototype":
        """Копия прототипа с тем же набором данных."""
        return filter_prototype(self.__source)

    def filter(self, dto: filter_dto) -> "filter_prototype":
        """Вернуть НОВЫЙ прототип с отфильтрованными данными."""
        filtered = [obj for obj in self.__source if self.__match(obj, dto)]
        return filter_prototype(filtered)

    def __match(self, obj: Any, dto: filter_dto) -> bool:
        value = self.__deep_value(obj, dto.field)
        if value is None:
            return False
        s = str(value)
        if dto.condition == filter_condition_enum.EQUALS:
            return s == dto.value
        if dto.condition == filter_condition_enum.LIKE:
            return dto.value.lower() in s.lower()
        return False

    def __deep_value(self, obj: Any, path: str) -> Any:
        for part in path.split("."):
            if obj is None:
                return None
            obj = getattr(obj, part, None)
        return obj


class balance_prototype(abstract_prototype):
    """Формирование ОСВ по списку объектов."""

    def process(self, source: list, dto: filter_dto | None = None) -> list[dict]:
        result = []
        for obj in source:
            h = sum(ord(c) for c in obj.id)
            opening = h % 100
            income = (h * 2) % 100
            expense = (h * 3) % 100
            result.append({
                "id": obj.id,
                "name": getattr(obj, "name", ""),
                "opening_balance": opening,
                "income": income,
                "expense": expense,
                "closing_balance": opening + income - expense,
            })
        return result
