from Src.Logics.storage_manager import storage_manager
from Src.Models.recipe_model import recipe_model
from Src.Models.ingredient_model import ingredient_model


def test_first_start_creates_recipe():
    """После convert(is_first=True) в менеджере есть хотя бы один рецепт."""
    m = storage_manager()
    m.convert(is_first=True)

    assert len(m.recipes) >= 1
    recipe = next(iter(m.recipes.values()))
    assert recipe.result is not None
    assert len(recipe.ingredients) > 0
    assert recipe.gross_weight > 0
    assert recipe.net_weight > 0


def test_first_start_creates_two_recipes_one_with_packaging():
    """Среди рецептов есть карта с упаковкой."""
    m = storage_manager()
    m.convert(is_first=True)

    assert len(m.recipes) >= 2
    # найдётся карта, где ингредиент относится к группе «Упаковка»
    has_packaging = any(
        ing.nomenclature.group is not None
        and ing.nomenclature.group.name == "Упаковка"
        for r in m.recipes.values()
        for ing in r.ingredients
    )
    assert has_packaging


def test_recipe_weights_change_on_add_and_remove():
    """Брутто/Нетто пересчитываются при add/remove ингредиента."""
    m = storage_manager()
    m.convert(is_first=True)
    recipe = next(iter(m.recipes.values()))
    before = recipe.gross_weight

    # удалить первый ингредиент
    first = recipe.ingredients[0]
    recipe.remove_ingredient(first.nomenclature)
    assert recipe.gross_weight < before

    # вернуть обратно
    recipe.add_ingredient(first)
    assert recipe.gross_weight == before
