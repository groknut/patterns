from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator


class reference_convertor(abstract_convertor):
    """Конвертор типа Reference — представление {id, name}."""

    def convert(self, object: Any) -> dict:
        validator.validate(object, abstract_model)
        return {"id": object.id, "name": getattr(object, "name", "")}
