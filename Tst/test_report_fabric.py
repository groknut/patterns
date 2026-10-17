import pytest

from Src.Core.abstract_report import abstract_report
from Src.Core.validator import argument_exception, validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Dtos.report_type_dto import report_type_enum
from Src.Logics.report_factory import report_factory
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report
from Src.Models.recipe_model import recipe_model


def checkReportSucces():
    report = report_factory()
    assert isinstance(report.create(report_type_enum.TXT), text_report)


def checkRaises():
    report = report_factory()
    with pytest.raises(argument_exception):
        assert isinstance(report.create(report_type_enum.TXT), text_report)


def checkReportSuccesWithCreateData():
    report = report_factory()
    assert isinstance(report.create(report_type_enum.TXT), text_report)

    m = storage_manager()
    m.convert(is_first=True)
    recipe = next(iter(m.recipes.values()))
    report = text_report()
    rep = report.build(recipe)

    assert rep.binary == []
    assert rep.text != ""
