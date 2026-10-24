from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor


class reference_convertor(abstract_convertor):
    """Глубокий конвертор доменной модели, списков и словарей."""

    @property
    def types(self) -> tuple[type, ...]:
        return (abstract_model, list, dict)

    def __init__(self) -> None:
        self.__field_convertors = [basic_convertor(), datetime_convertor()]

    def convert(self, object: Any) -> Any:
        """Запускает конвертацию."""
        return self.__convert(object, set())

    def __convert(self, object: Any, seen: set) -> Any:
        if isinstance(object, abstract_model):
            if object.id in seen:
                return {
                    "id": object.id,
                    "name": getattr(object, "name", ""),
                    "_circular": True
                }

            seen.add(object.id)
            result = {}
            for name, value in self.__iter_properties(object):
                result[name] = self.__convert(value, seen)
            seen.remove(object.id)
            return result

        elif isinstance(object, list):
            return [self.__convert(x, seen) for x in object]

        elif isinstance(object, dict):
            return {k: self.__convert(v, seen) for k, v in object.items()}

        else:
            convertor = self._find_convertor(object, self.__field_convertors)
            if convertor is None:
                return object

            res = convertor.convert(object)
            if isinstance(res, dict) and list(res.keys()) == ["value"]:
                return res["value"]
            return res

    def __iter_properties(self, obj):
        """Обходит @property и instance-атрибуты."""
        seen = set()
        for cls in type(obj).__mro__:
            for name, attr in vars(cls).items():
                if name in seen:
                    continue
                if isinstance(attr, property):
                    seen.add(name)
                    yield name, getattr(obj, name)
        for name, value in vars(obj).items():
            if name.startswith("_") or name in seen:
                continue
            seen.add(name)
            yield name, value
