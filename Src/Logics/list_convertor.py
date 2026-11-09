import typing
from typing import Any

from Src.Core.abstract_convertor import abstract_convertor


class list_convertor[T: list](abstract_convertor):
    """Конвертор списка — каждый элемент через фабрику."""

    def __init__(self, factory: abstract_convertor) -> None:
        self.__factory = factory

    @property
    def types(self) -> tuple[type, ...]:
        return (list, tuple)

    def convert(self, object: Any, _seen: set | None = None) -> list:
        return [self.__factory.convert(x, _seen) for x in object]

    def deserialize(self, source: dict, target_type: type[T], _seen: set | None = None) -> T:
        args = typing.get_args(target_type)
        if not args:
            return target_type(source)
        item_type = args[0]
        return [self.__factory.deserialize(x, item_type, _seen) for x in source]
