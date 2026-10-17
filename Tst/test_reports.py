from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report
from Src.Logics.csv_report import csv_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.xml_report import xml_report
from Src.Logics.html_report import html_report


def test_binary_reports_return_binary():
    """CSV и Markdown — binary заполнен, text пуст (для скачивания файла)."""
    settings_manager().load()
    storage_manager().convert(True)
    recipe = next(iter(storage_manager().recipes.values()))

    for report in (csv_report(), markdown_report()):
        result = report.build(recipe)
        assert result.text == ""
        assert len(result.binary) > 0


def test_text_reports_contain_all_ingredients():
    """TXT, XML, HTML — text заполнен, содержит все ингредиенты."""
    settings_manager().load()
    storage_manager().convert(True)
    recipe = next(iter(storage_manager().recipes.values()))

    for report in (text_report(), xml_report(), html_report()):
        result = report.build(recipe)
        assert result.text != ""
        assert result.binary == []
        for item in recipe.ingredients:
            assert item.name in result.text
