from typing import Any

from Src.Core.abstract_convertor import abstract_convertor


class dict_convertor(abstract_convertor):
    """Конвертор словаря — значения через фабрику."""

    def __init__(self, factory) -> None:
        self.__factory = factory

    @property
    def types(self) -> tuple[type, ...]:
        return (dict,)

    def convert(self, object: Any, _seen: set = None) -> dict:
        return {k: self.__factory.convert(v, _seen) for k, v in object.items()}
