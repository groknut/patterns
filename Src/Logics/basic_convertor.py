from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception


class basic_convertor(abstract_convertor):
    """Конвертор простых типов: int, float, str, bool."""

    types = (int, float, str, bool)

    def convert(self, object: Any) -> dict:
        if not isinstance(object, self.types):
            raise argument_exception(
                f"basic_convertor ожидает простой тип, получено "
                f"{type(object).__name__}"
            )
        return {"value": object}
