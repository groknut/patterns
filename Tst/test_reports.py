from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report
from Src.Logics.csv_report import csv_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.xml_report import xml_report
from Src.Logics.html_report import html_report


def _recipe():
    settings_manager().load()
    storage_manager().convert(True)
    return next(iter(storage_manager().recipes.values()))


def test_binary_reports_return_binary():
    """CSV и Markdown — binary заполнен, text пуст (задача 7)."""
    recipe = _recipe()
    for report in (csv_report(), markdown_report()):
        result = report.build(recipe)
        assert result.text == ""
        assert len(result.binary) > 0


def test_text_reports_return_text():
    """TXT, XML, HTML — text заполнен, binary пуст."""
    recipe = _recipe()
    for report in (text_report(), xml_report(), html_report()):
        result = report.build(recipe)
        assert result.text != ""
        assert result.binary == []


def test_all_reports_contain_all_ingredients():
    """В каждом отчёте присутствуют все id и name ингредиентов рецепта."""
    recipe = _recipe()
    results = [
        text_report().build(recipe).text,
        bytes(csv_report().build(recipe).binary).decode("utf-8"),
        bytes(markdown_report().build(recipe).binary).decode("utf-8"),
        xml_report().build(recipe).text,
        html_report().build(recipe).text,
    ]
    for text in results:
        for item in recipe.ingredients:
            assert item.id in text
            assert item.name in text


def test_report_weights_match_recipe_calculation():
    """Брутто/нетто в TXT-отчёте совпадают с расчётом recipe_model."""
    recipe = _recipe()
    text = text_report().build(recipe).text
    for item in recipe.ingredients:
        expected = (
            f"{item.id} | {item.name} | {item.gross_weight} | {item.net_weight}"
        )
        assert expected in text
