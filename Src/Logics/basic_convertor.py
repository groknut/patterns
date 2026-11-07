from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception


class basic_convertor[T: (int, float, str, bool)](abstract_convertor):
    """Конвертор для простых типов: numeric, str, bool"""

    @property
    def types(self) -> tuple[type, ...]:
        return (int, float, str, bool)

    def convert(self, object: Any, _seen: set | None = None) -> dict:
        if not isinstance(object, self.types):
            raise argument_exception(
                f"Ожидается простой тип, получено {type(object).__name__}"
            )
        return {"value": object}

    def deserialize(self, source: Any, target_type: type[T], _seen: set | None = None) -> T:
        if isinstance(source, dict) and "value" in source:
            return target_type(source["value"])
        return target_type(source)
