from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.dict_convertor import dict_convertor
from Src.Logics.list_convertor import list_convertor
from Src.Logics.reference_convertor import reference_convertor


class convert_factory(abstract_convertor):
    """Фабрика конверторов — диспетчер по типам."""

    __mapping: dict[type, abstract_convertor]= {}

    def __init__(self) -> None:

        self.__mapping = {}
        self.__register(basic_convertor())
        self.__register(datetime_convertor())
        self.__register(list_convertor(self))
        self.__register(dict_convertor(self))
        self.__register(reference_convertor(self))

    def __register(self, convertor: abstract_convertor):
        for type_ in convertor.types:
            self.__mapping[type_] = convertor

    def get_convertor(self, object) -> abstract_convertor:
        for cls in type(object).__mro__:
            if cls in self.__mapping:
                return self.__mapping[cls]
        raise argument_exception(
            f"Нет конвертора для типа {type(object).__name__}"
        )

    def convert(self, object: Any, _seen: set = None):
        """Делегирует конвертору, чей `types` подходит под объект."""
        return self.get_convertor(object).convert(object, _seen)

    @property
    def types(self) -> tuple[type, ...]:
        return ()
