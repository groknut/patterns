from datetime import date, datetime
from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import validator


class datetime_convertor(abstract_convertor):
    """Конвертор типа DateTime — ISO"""

    DATETIMES = (datetime, date)

    def convert(self, object: Any) -> dict:
        validator.validate(object, self.DATETIMES)
        return {"iso": object.isoformat()}
