from Src.Core.validator import argument_exception
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.convert_factory import convert_factory
from Src.Logics.reference_convertor import reference_convertor
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


def test_factory_get_convertor_for_primitive():
    """Фабрика корректно подбирает basic_convertor для int"""
    assert isinstance(convert_factory().get_convertor(42), basic_convertor)


def test_factory_get_convertor_for_nomenclature():
    """Фабрика корректно подбирает reference_convertor для модели"""
    g = group_model(name="Тест")
    r = range_model(name="штука", coef=1)
    nom = nomenclature_model(name="Тест", full_name="Тест", group=g, range=r)

    assert isinstance(convert_factory().get_convertor(nom), reference_convertor)


def test_convert_factory_for_primitive():
    """Верхний уровень: convert_factory(42) → {"value": 42}"""
    assert convert_factory().convert(42) == {"value": 42}


def test_convert_factory_for_nomenclature_model():
    """Составной объект: скалярные поля чистые, вложенные — развернуты"""
    g = group_model(name="Бакалея")
    r = range_model(name="килограмм", coef=1000)
    nom = nomenclature_model(
        full_name="Мука ржаная", name="Мука", group=g, range=r
    )

    result = convert_factory().convert(nom)

    assert result["id"] == nom.id
    assert result["name"] == "Мука"
    assert result["full_name"] == "Мука ржаная"

    assert result["group"]["id"] == g.id
    assert result["group"]["name"] == "Бакалея"

    assert result["range"]["name"] == "килограмм"
    assert result["range"]["coef"] == 1000.0


def test_factory_raise_for_unknown_type():
    """Фабрика бросает argument_exception, если нет подходящего конвертора"""
    try:
        convert_factory().get_convertor(None)
        assert False
    except argument_exception:
        assert True
