import pytest

from Src.Core.validator import argument_exception
from Src.Models.company_model import company_model


VALID_NAME = "ООО Ромашка"
VALID_INN = 123456789012  # 12 цифр
VALID_BIC = 123456789  # 9 цифр
VALID_CORR = 12345678901  # 11 цифр
VALID_ACC = 12345678901  # 11 цифр
VALID_OWN = "ООО"


@pytest.fixture
def valid_company() -> company_model:
    """Фикстура: полностью валидный объект company_model."""
    return company_model(
        name=VALID_NAME,
        inn=VALID_INN,
        bic=VALID_BIC,
        corr_account=VALID_CORR,
        account=VALID_ACC,
        ownership=VALID_OWN,
    )


def test_ValidData_CompanyModel_AllFieldsSaved(valid_company):
    """все переданные валидные поля сохраняются без изменений."""
    assert valid_company.name == VALID_NAME
    assert valid_company.inn == VALID_INN
    assert valid_company.bic == VALID_BIC
    assert valid_company.corr_account == VALID_CORR
    assert valid_company.account == VALID_ACC
    assert valid_company.ownership == VALID_OWN


@pytest.mark.parametrize("field", ["inn", "bic", "corr_account", "account"])
@pytest.mark.parametrize("value", [None, "123", [], True, 1.5, "345"])
def test_InvalidIntField_CompanyModel_RaisesArgumentException(field, value):
    """argument_exception при невалидном типе int-поля."""
    with pytest.raises(argument_exception):
        company_model(name=VALID_NAME, **{field: value})


@pytest.mark.parametrize("value", [None, 123, [], True, 1.5])
def test_InvalidOwnership_CompanyModel_RaisesArgumentException(value):
    """argument_exception при невалидном типе ownership."""
    with pytest.raises(argument_exception):
        company_model(name=VALID_NAME, ownership=value)


@pytest.mark.parametrize("value", ["А" * 6, "A" * 10])
def test_TooLongOwnership_CompanyModel_RaisesArgumentException(value):
    """argument_exception при превышении max_length ownership."""
    with pytest.raises(argument_exception):
        company_model(name=VALID_NAME, ownership=value)


def test_EmptyName_CompanyModel_RaisesArgumentException():
    """argument_exception при пустом name."""
    with pytest.raises(argument_exception):
        company_model(name="")
