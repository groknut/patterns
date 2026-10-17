from enum import Enum


class report_type_enum(Enum):
    """Тип отчета (формат вывода)"""

    TXT = "TXT"
    CSV = "CSV"
    MARKDOWN = "Markdown"
    XML = "XML"
    HTML = "HTML"

    @classmethod
    def from_str(cls, value) -> "report_type_enum":
        """Приводит строку (регистронезависимо) или член перечисления к члену перечисления."""
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().upper()
        for member in cls:
            if member.value.upper() == normalized:
                return member
        raise ValueError(f"Неизвестный формат отчета: {value}")
