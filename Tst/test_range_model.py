from Src.Models.range_model import range_model
import pytest
from Src.Core.exception import arguments_exception

def test_coef_setter_sets_new_value():
    """Сеттер coef меняет значение."""
    r = range_model("кг", 1000)
    r.coef = 500
    assert r.coef == 500.0
    assert isinstance(r.coef, float)

def test_coef_negative_raises():
    """Отрицательный коэффициент недопустим."""
    with pytest.raises(arguments_exception) as exc:
        range_model("кг", -5)
    assert exc.value.field == "coef"
