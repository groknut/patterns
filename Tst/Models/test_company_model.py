import pytest

from Src.Core.validator import (
    argument_exception
)
from Src.Models.company_model import company_model

VALID_NAME = "ООО Ромашка"
VALID_INN = 123456789012          # 12 цифр
VALID_BIC = 123456789             # 9 цифр
VALID_CORR = 12345678901          # 11 цифр
VALID_ACC = 12345678901           # 11 цифр
VALID_OWN = "ООО"


def make_company(**kwargs) -> company_model:
    name = kwargs.pop("name", VALID_NAME)
    obj = company_model(name=name)
    for field, value in kwargs.items():
        setattr(obj, field, value)
    return obj


def test_valid_company_all_fields():
    org = make_company(
        inn=VALID_INN,
        bic=VALID_BIC,
        corr_account=VALID_CORR,
        account=VALID_ACC,
        ownership=VALID_OWN,
    )
    assert org.inn == VALID_INN
    assert org.bic == VALID_BIC
    assert org.corr_account == VALID_CORR
    assert org.account == VALID_ACC
    assert org.ownership == VALID_OWN


@pytest.mark.parametrize("field", ["inn", "bic", "corr_account", "account"])
@pytest.mark.parametrize("value", [None, "123", [], True, 1.5, "345"])
def test_int_fields_invalid_type(field, value):
    with pytest.raises(argument_exception):
        make_company(**{field: value})


@pytest.mark.parametrize("value", [None, 123, [], True, 1.5])
def test_ownership_invalid_type(value):
    with pytest.raises(argument_exception):
        make_company(ownership=value)


@pytest.mark.parametrize("value", [None, 123, [], True])
def test_ownership_invalid_type(value):
    with pytest.raises(argument_exception):
        make_company(ownership=value)


@pytest.mark.parametrize("value", ["А" * 6, "A" * 10])
def test_ownership_too_long(value):
    with pytest.raises(argument_exception):
        make_company(ownership=value)


# def test_ownership_valid_and_strip():
#     for val in ["ООО", "А" * 5, " ООО "]:
#         org = make_company(ownership=val)
#         assert org.ownership == val.strip()


def test_empty_name_raises():
    with pytest.raises(argument_exception):
        company_model(name="")
