from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor


class convert_factory(abstract_convertor):
    """Фабрика конверторов — диспетчер по типам."""

    def __init__(self) -> None:
        self.__convertors = [
            basic_convertor(),
            datetime_convertor(),
            reference_convertor(),
        ]

    def get_convertor(self, object) -> abstract_convertor:
        convertor = self._find_convertor(object, self.__convertors)
        if convertor is None:
            raise argument_exception(
                f"Нет конвертора для типа {type(object).__name__}"
            )
        return convertor

    def convert(self, object: Any):
        """Делегирует конвертору, чей `types` подходит под объект."""
        return self.get_convertor(object).convert(object)

    @property
    def types(self) -> tuple[type, ...]:
        return ()
