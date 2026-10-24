from Src.Logics.reference_convertor import reference_convertor
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


def test_convert_reference_convertor_for_group_model():
    """reference_convertor(group_model) → все поля (id, name)"""
    g = group_model(name="Бакалея")
    result = reference_convertor().convert(g)

    assert result["id"] == {"value": g.id}
    assert result["name"] == {"value": "Бакалея"}


def test_convert_reference_convertor_for_nested_base():
    """reference_convertor разворачивает глубокую цепочку Base → Base"""
    gramm = range_model(name="грамм", coef=1)
    kg = range_model(name="килограмм", coef=1000, base=gramm)

    result = reference_convertor().convert(kg)

    assert result["name"] == {"value": "килограмм"}
    assert result["coef"] == {"value": 1000.0}
    assert result["base"]["name"] == {"value": "грамм"}
    assert result["base"]["coef"] == {"value": 1.0}
