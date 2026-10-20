from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import report_type_enum
from Src.Logics.report_factory import report_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.text_report import text_report


def test_create_txt_returns_text_report():
    """create() — успешно возвращается text_report"""
    factory = report_factory()
    report = factory.create(report_type_enum.TXT)
    assert isinstance(report, text_report)


def test_create_unknown_format_raises():
    """create() - неизвестный формат"""
    factory = report_factory()
    try:
        factory.create("PDF")
        assert False
    except argument_exception:
        assert True


def test_default_uses_txt_from_settings():
    """create_default() — формат берётся из настроек"""
    manager = settings_manager()
    try:
        manager.load()
    except argument_exception:
        assert False

    manager.settings.response_format = report_type_enum.TXT
    factory = report_factory()
    assert isinstance(factory.create_default(), text_report)
