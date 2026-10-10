import pytest

from Src.Core.validator import argument_exception
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model


GRAM = range_model(name="грамм", coef=1)
KILOGRAM = range_model(name="килограмм", coef=1000, base=GRAM)


def make_nomenclature(name: str = "Мука ржаная") -> nomenclature_model:
    """Сделать номенклатуру"""
    return nomenclature_model(
        name,
        f"{name} (полное наименование)",
        group_model(name="Бакалея"),
        KILOGRAM,
    )


def make_ingredient(
    name: str = "Мука", quantity: float = 0.2, loss_ratio: float = 0.0
) -> ingredient_model:
    """Сделать ингредиент"""
    nom = make_nomenclature(name)
    return ingredient_model(
        nomenclature=nom, range_=nom.range, quantity=quantity, loss_ratio=loss_ratio
    )


def make_recipe(**overrides) -> recipe_model:
    """Создать рецепт"""
    params = {
        "name": "Оладьи пышные",
        "result": make_nomenclature("Оладьи пышные"),
        "output_quantity": 1,
        "cooking_time_minutes": 30,
        "steps": ["Замесить тесто", "Обжарить"],
    }
    params.update(overrides)
    return recipe_model(**params)


def test_init_valid_params_fields_set():
    """Карта создаётся с переданными полями, пустым составом и id."""
    result = make_nomenclature("Оладьи пышные")
    r = recipe_model("Оладьи", result, 1, 30, ["Замесить", "Обжарить"])

    assert r.name == "Оладьи"
    assert r.result is result
    assert r.output_quantity == 1
    assert r.cooking_time_minutes == 30
    assert r.steps == ["Замесить", "Обжарить"]
    assert r.ingredients == []
    assert r.id is not None


@pytest.mark.parametrize("value", [0, -1, None, "1"])
def test_init_invalid_output_quantity_raises(value):
    """Некорректный выход вызывает argument_exception."""
    with pytest.raises(argument_exception):
        make_recipe(output_quantity=value)


@pytest.mark.parametrize("steps", [None, [], [1], ["Нарезать", None]])
def test_init_invalid_steps_raises(steps):
    """Некорректные шаги вызывают argument_exception."""
    with pytest.raises(argument_exception):
        make_recipe(steps=steps)


def test_result_setter_not_allowed_raises():
    """Результат карты нельзя заменить."""
    r = make_recipe()
    with pytest.raises(AttributeError):
        r.result = make_nomenclature("Другое")


def test_add_and_remove_ingredient_constraints():
    """Уникальность по номенклатуре, защита от самоссылки, удаление по номенклатуре."""
    nom = make_nomenclature("Мука")
    r = make_recipe(
        ingredients=[ingredient_model(nomenclature=nom, range_=nom.range, quantity=0.1)]
    )

    # дубликат номенклатуры
    with pytest.raises(argument_exception):
        r.add_ingredient(
            ingredient_model(nomenclature=nom, range_=nom.range, quantity=0.2)
        )

    # результат карты как ингредиент
    with pytest.raises(argument_exception):
        r.add_ingredient(
            ingredient_model(nomenclature=r.result, range_=r.result.range, quantity=1)
        )

    # удаление существующей — ок, повторное — ошибка
    r.remove_ingredient(nom)
    assert r.ingredients == []
    with pytest.raises(argument_exception):
        r.remove_ingredient(nom)


def test_weights_summed_and_recalculated():
    """Брутто и нетто карты — суммы по ингредиентам, пересчитываются при изменениях."""
    a = make_ingredient("Мука", 0.2, 0.2)  # брутто 200, нетто 160
    b = make_ingredient("Кефир", 0.25, 0.2)  # брутто 250, нетто 200
    r = make_recipe(ingredients=[a, b])

    assert r.gross_weight == pytest.approx(450)
    assert r.net_weight == pytest.approx(360)

    # изменение ингредиента, лежащего в карте
    a.quantity = 0.5
    a.loss_ratio = 0.4
    assert r.gross_weight == pytest.approx(750)
    assert r.net_weight == pytest.approx(500)

    # удаление ингредиента
    r.remove_ingredient(b.nomenclature)
    assert r.gross_weight == pytest.approx(500)
    assert r.net_weight == pytest.approx(300)
