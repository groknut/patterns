from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.model_convertor import model_convertor


class convert_factory(abstract_convertor):
    """Фабрика конверторов — диспетчер по типам."""

    types = ()

    def __init__(self) -> None:
        self.__convertors = [
            basic_convertor(),
            datetime_convertor(),
            model_convertor(),
        ]

    def convert(self, object: Any) -> dict:
        """Делегирует конвертору, чей `types` подходит под объект."""
        convertor = self.__find_convertor(object)
        if convertor is None:
            raise argument_exception(
                f"convert_factory не поддерживает тип {type(object).__name__}"
            )
        return convertor.convert(object)

    def __find_convertor(self, obj):
        return next(
            (c for c in self.__convertors if isinstance(obj, c.types)), None
        )
