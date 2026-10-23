from Src.Logics.model_convertor import model_convertor
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


def test_convert_model_convertor_for_nomenclature_model():
    """model_convertor обходит @property и делегирует поля конверторам"""
    g = group_model(name="Бакалея")
    r = range_model(name="килограмм", coef=1000)
    nom = nomenclature_model(
        full_name="Мука ржаная", name="Мука", group=g, range=r
    )

    result = model_convertor().convert(nom)

    assert result["name"] == {"value": "Мука"}
    assert result["group"] == {"id": g.id, "name": "Бакалея"}
    assert result["range"] == {"id": r.id, "name": "килограмм"}
