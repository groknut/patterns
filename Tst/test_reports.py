from Src.Core.validator import argument_exception
from Src.Logics.csv_report import csv_report
from Src.Logics.html_report import html_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.report_sources import recipe_report_source
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report
from Src.Logics.xml_report import xml_report


def _recipe():
    """Возвращает первый рецепт из storage_manager после инициализации."""
    settings_manager().load()
    storage_manager().convert(True)
    return next(iter(storage_manager().recipes.values()))


def test_binary_reports_return_binary():
    """CSV и Markdown отдают binary, text пуст — форматы для скачивания файла."""
    source = recipe_report_source(_recipe())
    for report in (csv_report(), markdown_report()):
        result = report.build(source)
        assert result.text == ""
        assert len(result.binary) > 0


def test_text_reports_return_text():
    """TXT, XML и HTML отдают text, binary пуст — структурированный текст."""
    source = recipe_report_source(_recipe())
    for report in (text_report(), xml_report(), html_report()):
        result = report.build(source)
        assert result.text != ""
        assert result.binary == []


def test_all_reports_contain_all_ingredients():
    """В каждом из 5 форматов присутствуют id и name всех ингредиентов рецепта."""
    recipe = _recipe()
    source = recipe_report_source(recipe)

    results = [
        text_report().build(source).text,
        bytes(csv_report().build(source).binary).decode("utf-8"),
        bytes(markdown_report().build(source).binary).decode("utf-8"),
        xml_report().build(source).text,
        html_report().build(source).text,
    ]
    for text in results:
        for item in recipe.ingredients:
            assert item.id in text
            assert item.name in text


def test_report_weights_match_recipe_calculation():
    """Брутто и нетто в TXT-отчёте совпадают с расчётом recipe_model."""
    recipe = _recipe()
    source = recipe_report_source(recipe)
    text = text_report().build(source).text

    for item in recipe.ingredients:
        expected = f"{item.id} | {item.name} | {item.gross_weight} | {item.net_weight}"
        assert expected in text


def test_recipe_report_source_headers_and_rows():
    """recipe_report_source отдаёт заголовки и строки по ингредиентам рецепта."""
    recipe = _recipe()
    source = recipe_report_source(recipe)

    assert source.report_headers() == ["Код", "Наименование", "Брутто", "Нетто"]
    assert len(source.report_rows()) == len(recipe.ingredients)


def test_text_report_unknown_entity_raises():
    """text_report.build() бросает argument_exception на не-report_source объекте."""
    try:
        text_report().build("not-a-model")
        assert False
    except argument_exception:
        assert True
