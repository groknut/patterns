from typing import Any

from Src.Core.abstract_filter_prototype import abstract_filter_prototype
from Src.Dtos.filter_dto import filter_condition_enum, filter_dto


class filter_prototype(abstract_filter_prototype):
    """Универсальный фильтр для всех доменных моделей."""

    def filter(self, objects: list, dto: filter_dto) -> list:
        result = []
        for obj in objects:
            val = self.__get_deep_value(obj, dto.field)
            if self.__match(val, dto.value, dto.condition):
                result.append(obj)
        return result

    def __get_deep_value(self, obj: Any, path: str) -> Any:
        """Извлекает значение по пути (например, 'base.name')."""
        current = obj
        for part in path.split("."):
            if current is None:
                return None
            current = getattr(current, part, None)
        return current

    @staticmethod
    def __match(obj_val: Any, filter_val: str, condition: filter_condition_enum) -> bool:
        if obj_val is None:
            return False
        str_val = str(obj_val)
        if condition == filter_condition_enum.EQUALS:
            return str_val == filter_val
        if condition == filter_condition_enum.LIKE:
            return filter_val.lower() in str_val.lower()
        return False
