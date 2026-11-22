from datetime import date

from Src.Dtos.balance_dto import balance_dto
from Src.Dtos.filter_condition_enum import filter_condition_enum
from Src.Dtos.filter_dto import filter_dto
from Src.Models.movement_model import movement_model, movement_operation_enum
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Services.balance_service import balance_service


def test_balance_service_returns_balance_dto():
    """balance_service возвращает список balance_dto"""
    g = group_model(name="Бакалея")
    r = range_model(name="кг", coef=1000)
    nom = nomenclature_model(full_name="Мука", name="Мука", group=g, range=r)

    movements = [
        movement_model(
            date=date(2024, 1, 10), nomenclature=nom, quantity=100,
            operation=movement_operation_enum.INCOME,
        ),
        movement_model(
            date=date(2024, 3, 20), nomenclature=nom, quantity=15,
            operation=movement_operation_enum.EXPENSE,
        ),
        ]

    dto = filter_dto(field="name", value="Мука", condition=filter_condition_enum.EQUALS)
    result = balance_service().build(
        movements, dto,
        start_date=date(2024, 3, 1),
        end_date=date(2024, 3, 31),
        )

    assert len(result) == 1
    assert isinstance(result[0], balance_dto)
    assert result[0].name == "Мука"
    assert result[0].unit == "кг"
    assert result[0].closing_balance == (
        result[0].opening_balance + result[0].income - result[0].expense
    )
