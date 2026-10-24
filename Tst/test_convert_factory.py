from Src.Core.validator import argument_exception
from Src.Logics.convert_factory import convert_factory
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


def test_convert_factory_for_primitive():
    """convert_factory(42) → {"value": 42} (подбор basic_convertor)"""
    assert convert_factory().convert(42) == {"value": 42}


def test_convert_factory_for_nomenclature_model():
    """Составной объект: простые поля + глубокий обход ссылок (group, range)"""
    g = group_model(name="Бакалея")
    r = range_model(name="килограмм", coef=1000)
    nom = nomenclature_model(
        full_name="Мука ржаная", name="Мука", group=g, range=r
    )

    result = convert_factory().convert(nom)

    assert result["name"] == "Мука"
    assert result["group"]["name"] == "Бакалея"
    assert result["range"]["coef"] == 1000.0


def test_factory_raise_for_unknown_type():
    """Фабрика бросает argument_exception, если нет подходящего конвертора"""
    try:
        convert_factory().get_convertor(None)
        assert False
    except argument_exception:
        assert True
