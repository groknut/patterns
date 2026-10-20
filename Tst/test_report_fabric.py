from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import report_type_enum
from Src.Logics.report_factory import report_factory
from Src.Logics.report_sources import recipe_report_source
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report


def test_report_succes():
    """create() — для TXT возвращается text_report"""
    report = report_factory()
    assert isinstance(report.create(report_type_enum.TXT), text_report)


def test_raises():
    """create() — на неизвестном формате бросается argument_exception"""
    report = report_factory()
    try:
        report.create("PDF")
        assert False
    except argument_exception:
        assert True


def test_report_succes_with_create_data():
    """build() — рецепт из storage даёт непустой text и пустой binary"""
    report = report_factory()
    assert isinstance(report.create(report_type_enum.TXT), text_report)

    m = storage_manager()
    m.convert(True)
    recipe = next(iter(m.recipes.values()))
    source = recipe_report_source(recipe)
    report = text_report()
    rep = report.build(source)

    assert rep.binary == []
    assert rep.text != ""
