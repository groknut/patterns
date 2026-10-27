from typing import Any

from Src.Core.abstract_convertor import abstract_convertor


class list_convertor(abstract_convertor):
    """Конвертор списка — каждый элемент через фабрику."""

    def __init__(self, factory: abstract_convertor) -> None:
        self.__factory = factory

    @property
    def types(self) -> tuple[type, ...]:
        return (list, tuple)

    def convert(self, object: Any, _seen: set = None) -> list:
        return [self.__factory.convert(x, _seen) for x in object]
