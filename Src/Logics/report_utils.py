from Src.Core.validator import argument_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model


def extract_table(source) -> tuple[list[str], list[list[str]]]:
    """Возвращает (headers, rows) для доменной сущности."""
    if isinstance(source, recipe_model):
        return _recipe_table(source)
    if isinstance(source, nomenclature_model):
        return _nomenclature_table(source)
    if isinstance(source, range_model):
        return _range_table(source)
    raise argument_exception(
        f"Тип «{type(source).__name__}» не поддерживается для формирования отчета"
    )


def _recipe_table(recipe: recipe_model):
    headers = ["Код", "Наименование", "Брутто", "Нетто"]
    rows = [
        [item.id, item.name, str(item.gross_weight), str(item.net_weight)]
        for item in recipe.ingredients
    ]
    return headers, rows


def _nomenclature_table(nom: nomenclature_model):
    headers = ["Код", "Наименование", "Полное наименование", "Группа", "Ед. изм."]
    rows = [[
        nom.id,
        nom.name,
        nom.full_name,
        nom.group.name if nom.group else "",
        nom.range.name if nom.range else "",
    ]]
    return headers, rows


def _range_table(rng: range_model):
    headers = ["Код", "Наименование", "Коэффициент", "Базовая единица"]
    rows = [[
        rng.id,
        rng.name,
        str(rng.coef),
        rng.base.name if rng.base else "-",
    ]]
    return headers, rows
