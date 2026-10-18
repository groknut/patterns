from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report
from Src.Logics.report_sources import recipe_report_source


def test_build_txt_from_storage_returns_text():
    """build() — рецепт из storage даёт непустой text и пустой binary"""
    m = storage_manager()
    m.convert(True)
    recipe = next(iter(m.recipes.values()))
    source = recipe_report_source(recipe)
    report = text_report()
    rep = report.build(source)

    assert rep.binary == []
    assert rep.text != ""
