from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_condition_enum import filter_condition_enum
from Src.Logics.prototypes import filter_prototype
from Src.Models.group_model import group_model


def test_filter_equals_exact_match():
    """EQUALS: полное совпадение имени"""
    objects = [group_model(name="Бакалея"), group_model(name="Молочные")]
    dto = filter_dto(field="name", value="Бакалея", condition=filter_condition_enum.EQUALS)

    result = filter_prototype(objects).filter(dto).data

    assert len(result) == 1
    assert result[0].name == "Бакалея"


def test_filter_like_case_insensitive():
    """LIKE: вхождение подстроки без учёта регистра"""
    objects = [group_model(name="Бакалея"), group_model(name="Молочные")]
    dto = filter_dto(field="name", value="МОЛОЧ", condition=filter_condition_enum.LIKE)

    result = filter_prototype(objects).filter(dto).data
    assert len(result) == 1
    assert result[0].name == "Молочные"

def test_clone_returns_new_instance():
    """clone() возвращает новый объект того же класса с тем же data"""
    proto = filter_prototype([group_model(name="А")])
    copy = proto.clone()

    assert isinstance(copy, filter_prototype)
    assert copy is not proto
    assert len(copy.data) == 1
