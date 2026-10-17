from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report
from Src.Models.recipe_model import recipe_model


def test_checkReport():
    m = storage_manager()
    m.convert(is_first=True)
    recipe = next(iter(m.recipes.values()))
    report = text_report()
    rep = report.build(recipe)

    assert rep.binary == []
    assert rep.text != ""
