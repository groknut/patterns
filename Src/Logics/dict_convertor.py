import typing
from typing import Any

from Src.Core.abstract_convertor import abstract_convertor


class dict_convertor[T: dict](abstract_convertor):
    """Конвертор словаря — значения через фабрику."""

    def __init__(self, factory: abstract_convertor) -> None:
        self.__factory = factory

    @property
    def types(self) -> tuple[type, ...]:
        return (dict,)

    def convert(self, object: Any, _seen: set | None = None) -> dict:
        return {k: self.__factory.convert(v, _seen) for k, v in object.items()}

    def deserialize(
        self, source: dict, target_type: type, _seen: set | None = None
    ) -> dict:
        args = typing.get_args(target_type)
        if len(args) != 2:
            return dict(source)
        val_type = args[1]
        return {
            k: self.__factory.deserialize(v, val_type, _seen)
            for k, v in source.items()
        }
