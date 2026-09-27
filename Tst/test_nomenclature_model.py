import pytest

from Src.Core.exception import arguments_exception, max_len_exception
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model


def test_valid_result_nomenclature_model_correct():
    """
    Проверяет, что номенклатура с корректными полями создаётся.
    """
    group = group_model("Продукты")
    measure = range_model("кг", 1000)
    item = nomenclature_model(
        full_name="Сахар-песок белый",
        name="Сахар",
        group=group,
        range=measure
    )

    assert item.name == "Сахар"
    assert item.full_name == "Сахар-песок белый"
    assert item.group is group
    assert item.range is measure


def test_invalid_result_nomenclature_model_full_name_type_arguments_exception():
    """
    Проверяет, что не-строка в full_name даёт arguments_exception.
    """
    with pytest.raises(arguments_exception):
        nomenclature_model(name="Сахар", full_name=None)


def test_invalid_result_nomenclature_model_full_name_max_len_exception():
    """
    Проверяет, что full_name длиннее 255 символов даёт max_len_exception.
    """
    with pytest.raises(max_len_exception):
        nomenclature_model(name="Сахар", full_name="А" * 256)
