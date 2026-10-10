import pytest

from Src.Core.validator import argument_exception
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.ingredient_model import ingredient_model

GRAM = range_model(name="грамм", coef=1)
KILOGRAM = range_model(name="килограмм", coef=1000, base=GRAM)
PIECE = range_model(name="штука", coef=1)

def make_nomenclature(
    name: str = "Мука ржаная", rng: range_model = KILOGRAM
) -> nomenclature_model:
    return nomenclature_model(
        name,
        f"{name} (полное наименование)",
        group_model(name="Бакалея"),
        rng,
    )


def make_ingredient(**overrides) -> ingredient_model:
    nom = overrides.pop("nomenclature", make_nomenclature())
    params = {
        "nomenclature": nom,
        "range_": nom.range,
        "quantity": 0.2,
        "loss_ratio": 0.0,
        "grams_per_unit": None,
    }
    params.update(overrides)
    return ingredient_model(**params)


def test_ValidParams_IngredientModel_FieldsSet():
    """Ингредиент создаётся с переданными полями."""
    nom = make_nomenclature()
    ing = ingredient_model(
        nomenclature=nom, range_=nom.range, quantity=0.2, loss_ratio=0.25
    )

    assert ing.nomenclature is nom
    assert ing.range is nom.range
    assert ing.quantity == 0.2
    assert ing.loss_ratio == 0.25


@pytest.mark.parametrize("quantity", [0, -1, None, "80"])
@pytest.mark.parametrize("loss_ratio", [-0.1, 1, None, "0.1"])
def test_InvalidQuantityOrLoss_IngredientModel_RaisesArgumentException(quantity, loss_ratio):
    """Некорректные количество и доля потерь вызывают argument_exception."""
    with pytest.raises(argument_exception):
        make_ingredient(quantity=quantity, loss_ratio=loss_ratio)


def test_ValidSetters_IngredientModel_ValuesUpdated():
    """Сеттеры обновляют количество и долю потерь."""
    ing = make_ingredient(quantity=0.1, loss_ratio=0.1)
    ing.quantity = 0.3
    ing.loss_ratio = 0.4
    assert ing.quantity == 0.3
    assert ing.loss_ratio == 0.4


def test_GrossWeight_IngredientModel_FromRangeAndGramsPerUnit():
    """Брутто = количество × grams_per_unit (из range_model или заданный явно)."""
    kg = make_ingredient(quantity=0.2)  # 0.2 кг × 1000 = 200
    egg = make_ingredient(
        nomenclature=make_nomenclature("Яйцо", PIECE),
        quantity=2,
        grams_per_unit=10.0,
    )  # 2 × 10 = 20
    assert kg.gross_weight == pytest.approx(200)
    assert egg.gross_weight == pytest.approx(20)


def test_NetWeight_IngredientModel_WithLossAndRecalc():
    """Нетто = брутто × (1 − loss_ratio), пересчитывается при смене полей."""
    ing = make_ingredient(quantity=0.1, loss_ratio=0.2)
    assert ing.net_weight == pytest.approx(80)

    ing.quantity = 0.2
    ing.loss_ratio = 0.5
    assert ing.gross_weight == pytest.approx(200)
    assert ing.net_weight == pytest.approx(100)
