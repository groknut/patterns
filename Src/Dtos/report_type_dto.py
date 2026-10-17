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
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().upper()
        for member in cls:
            if member.value.upper() == normalized:
                return member
        raise ValueError(f"Неизвестный формат отчета: {value}")


class entity_type_enum(Enum):
    """Тип сущности для формирования отчета"""

    NOMENCLATURE = "nomenclature"
    RANGE = "range"
    RECIPE = "recipe"

    @classmethod
    def from_str(cls, value) -> "entity_type_enum":
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().lower()
        for member in cls:
            if member.value.lower() == normalized:
                return member
        aliases = {
            "номенклатура": cls.NOMENCLATURE,
            "номенклатуры": cls.NOMENCLATURE,
            "единица": cls.RANGE,
            "единица измерения": cls.RANGE,
            "рецепт": cls.RECIPE,
        }
        if normalized in aliases:
            return aliases[normalized]
        raise ValueError(f"Неизвестный тип сущности: {value}")
