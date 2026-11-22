from datetime import date as date_type
from enum import Enum

from Src.Core.entity_model import entity_model
from Src.Core.validator import argument_exception, validator
from Src.Models.nomenclature_model import nomenclature_model


class movement_operation_enum(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    @classmethod
    def from_str(cls, value) -> "movement_operation_enum":
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().upper()
        for member in cls:
            if member.value.upper() == normalized:
                return member
        raise ValueError(f"Неизвестная операция движения: {value}")


class movement_model(entity_model):
    """Движение товара (проводка) — источник данных для ОСВ."""

    __date: date_type = None
    __nomenclature: nomenclature_model = None
    __quantity: float = 0.0
    __operation: movement_operation_enum = movement_operation_enum.INCOME

    def __init__(self, date=None, nomenclature=None, quantity=0.0,
                 operation=movement_operation_enum.INCOME) -> None:
        super().__init__()
        if date is not None:
            self.date = date
        if nomenclature is not None:
            self.nomenclature = nomenclature
            self.name = nomenclature.name
        self.quantity = quantity
        self.operation = operation

    @property
    def date(self) -> date_type:
        return self.__date

    @date.setter
    def date(self, value) -> None:
        validator.validate(value, date_type)
        self.__date = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value) -> None:
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value) -> None:
        validator.validate(value, (int, float))
        if value <= 0:
            raise argument_exception("Количество должно быть больше нуля")
        self.__quantity = float(value)

    @property
    def operation(self) -> movement_operation_enum:
        return self.__operation

    @operation.setter
    def operation(self, value) -> None:
        if isinstance(value, str):
            value = movement_operation_enum.from_str(value)
        validator.validate(value, movement_operation_enum)
        self.__operation = value

    @staticmethod
    def create_sample_movements(nomenclatures: list) -> list["movement_model"]:
        """Демо-движения: 2 прихода (янв, фев) + 1 расход (март)."""
        movements: list[movement_model] = []
        for nom in nomenclatures:
            h = sum(ord(c) for c in nom.id)
            movements.append(movement_model(
                date=date_type(2024, 1, 15), nomenclature=nom,
                quantity=(h % 50) + 100, operation=movement_operation_enum.INCOME,
            ))
            movements.append(movement_model(
                date=date_type(2024, 2, 10), nomenclature=nom,
                quantity=(h % 30) + 20, operation=movement_operation_enum.INCOME,
            ))
            movements.append(movement_model(
                date=date_type(2024, 3, 20), nomenclature=nom,
                quantity=(h % 15) + 5, operation=movement_operation_enum.EXPENSE,
            ))
        return movements
