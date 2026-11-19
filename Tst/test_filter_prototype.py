from Src.Dtos.filter_dto import filter_condition_enum, filter_dto
from Src.Logics.prototypes import balance_prototype, filter_prototype
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model


def test_filter_equals_exact_match():
    """EQUALS: полное совпадение имени"""
    objects = [group_model(name="Бакалея"), group_model(name="Молочные")]
    dto = filter_dto(field="name", value="Бакалея", condition=filter_condition_enum.EQUALS)

    result = filter_prototype().process(objects, dto)

    assert len(result) == 1
    assert result[0].name == "Бакалея"


def test_filter_like_case_insensitive():
    """LIKE: вхождение подстроки без учёта регистра"""
    objects = [group_model(name="Бакалея"), group_model(name="Молочные")]
    dto = filter_dto(field="name", value="МОЛОЧ", condition=filter_condition_enum.LIKE)

    result = filter_prototype().process(objects, dto)

    assert len(result) == 1
    assert result[0].name == "Молочные"

def test_balance_returns_all_columns():
    objects = [group_model(name="Бакалея")]
    result = balance_prototype().process(objects)

    assert len(result) == 1
    assert set(result[0].keys()) == {
        "id", "name", "opening_balance", "income", "expense", "closing_balance"
    }
