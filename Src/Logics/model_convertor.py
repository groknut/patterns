from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor


class model_convertor(abstract_convertor):
    """Конвертор доменной модели — обход @property и делегирование полей."""

    types = (abstract_model,)

    def __init__(self) -> None:
        """Инициализирует конверторы полей"""
        self.__field_convertors = [
            basic_convertor(),
            datetime_convertor(),
            reference_convertor(),
        ]

    def convert(self, object: Any) -> dict:
        """Обходит @property модели, каждое поле — через подходящий конвертор."""
        result = {}
        for name, value in self.__iter_properties(object):
            convertor = self.__find_convertor(value)
            if convertor is not None:
                result[name] = convertor.convert(value)
        return result

    def __find_convertor(self, obj):
        return next(
            (c for c in self.__field_convertors if isinstance(obj, c.types)),
            None,
        )

    def __iter_properties(self, obj):
        seen = set()
        for cls in type(obj).__mro__:
            for name, attr in vars(cls).items():
                if name in seen:
                    continue
                if isinstance(attr, property):
                    seen.add(name)
                    yield name, getattr(obj, name)
