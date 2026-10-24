from datetime import date, datetime
from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception


class datetime_convertor(abstract_convertor):
    @property
    def types(self) -> tuple[type, ...]:
        return (datetime, date)

    def convert(self, object: Any) -> dict:
        if not isinstance(object, self.types):
            raise argument_exception(f"Ожидается дата, получено {type(object).__name__}")
        return {"iso": object.isoformat()}
