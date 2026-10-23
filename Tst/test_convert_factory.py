from Src.Logics.convert_factory import convert_factory
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


def test_convert_factory_for_primitive():
    """convert_factory(42) → {"value": 42}"""
    assert convert_factory().convert(42) == {"value": 42}


def test_convert_factory_for_nomenclature_model():
    """Составной объект: простые поля + ссылки group и range"""
    g = group_model(name="Бакалея")
    r = range_model(name="килограмм", coef=1000)
    nom = nomenclature_model(
        full_name="Мука ржаная", name="Мука", group=g, range=r
    )

    result = convert_factory().convert(nom)

    assert result["id"] == {"value": nom.id}
    assert result["name"] == {"value": "Мука"}
    assert result["full_name"] == {"value": "Мука ржаная"}
    assert result["group"] == {"id": g.id, "name": "Бакалея"}
    assert result["range"] == {"id": r.id, "name": "килограмм"}
