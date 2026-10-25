from Src.Logics.convert_factory import convert_factory
from Src.Logics.reference_convertor import reference_convertor
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model


def test_convert_reference_convertor_for_group_model():
    """group_model разворачивается в {id, name}"""
    g = group_model(name="Бакалея")
    factory = convert_factory()
    convertor = reference_convertor(factory)

    result = convertor.convert(g)

    assert result["id"] == g.id
    assert result["name"] == "Бакалея"


def test_convert_reference_convertor_for_nested_base():
    """Цепочка Base → Base разворачивается рекурсивно"""
    gramm = range_model(name="грамм", coef=1)
    kg = range_model(name="килограмм", coef=1000, base=gramm)
    factory = convert_factory()
    convertor = reference_convertor(factory)

    result = convertor.convert(kg)

    assert result["name"] == "килограмм"
    assert result["coef"] == 1000.0
    assert result["base"]["name"] == "грамм"
    assert result["base"]["coef"] == 1.0
