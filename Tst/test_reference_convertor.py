from Src.Logics.reference_convertor import reference_convertor
from Src.Models.company_model import company_model
from Src.Models.group_model import group_model


def test_wrap_value_reference_convertor_for_group_model():
    """reference_convertor(group_model) → {"id": ..., "name": "Бакалея"}"""
    g = group_model(name="Бакалея")
    assert reference_convertor().convert(g) == {"id": g.id, "name": "Бакалея"}


def test_wrap_value_reference_convertor_for_company_model():
    """reference_convertor(company_model) → {"id": ..., "name": "ООО Ромашка"}"""
    c = company_model(name="ООО Ромашка")
    assert reference_convertor().convert(c) == {"id": c.id, "name": "ООО Ромашка"}
