from typing import Any

from Src.Core.abstract_prototype import abstract_prototype
from Src.Dtos.filter_dto import filter_condition_enum, filter_dto


class filter_prototype(abstract_prototype):
    """Фильтрация объектов по DTO."""

    def process(self, source: list, dto: filter_dto | None = None) -> list:
        if dto is None:
            return list(source)
        return [obj for obj in source if self.__match(obj, dto)]

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
