import pytest

from Src.Core.exception import (
    arguments_exception,
    len_exception,
    max_len_exception,
    validation_exception,
)
from Src.Models.organization_model import organization_model

VALID_INN = "7707083893"
VALID_BIC = "044525225"
VALID_ACCOUNT = "40702810900000000000"
VALID_OWNER = "ООО"

def _make_organization(**kwargs) -> organization_model:
    """
    Хелпер: создаёт организацию с корректными реквизитами
    """
    defaults = dict(
        name="ООО Ромашка",
        inn=VALID_INN,
        bic=VALID_BIC,
        account=VALID_ACCOUNT,
        owner=VALID_OWNER,
    )
    defaults.update(kwargs)
    return organization_model(**defaults)


def test_valid_result_organization_model_all_fields_correct():
    """
    Проверяет, что организация с корректными реквизитами создаётся.
    """
    org = _make_organization()
    assert org.inn == VALID_INN
    assert org.bic == VALID_BIC
    assert org.account == VALID_ACCOUNT
    assert org.owner == VALID_OWNER


@pytest.mark.parametrize("value, exc_type", [
    (None, arguments_exception),
    (123, arguments_exception),
    ([], arguments_exception),
    (True, arguments_exception),
    ("", len_exception),
    ("12345", len_exception),
    ("1" * 11, len_exception),
    ("abcdefghij", validation_exception),
    ("7707 83893", validation_exception),
    ("7707083894", validation_exception),
    ("1234567890", validation_exception),
])
def test_invalid_result_organization_model_inn(value, exc_type):
    """
    Проверяет все сценарии невалидного ИНН.
    """
    with pytest.raises(exc_type):
        _make_organization(inn=value)


@pytest.mark.parametrize("value, exc_type", [
    (None, arguments_exception),
    (123, arguments_exception),
    ([], arguments_exception),
    (True, arguments_exception),
    ("", len_exception),
    ("12345678", len_exception),
    ("1" * 10, len_exception),
    ("abcdefghi", validation_exception),
    ("0445 2525", validation_exception),
])
def test_invalid_result_organization_model_bic(value, exc_type):
    """
    Проверяет все сценарии невалидного БИК.
    """
    with pytest.raises(exc_type):
        _make_organization(bic=value)


@pytest.mark.parametrize("value, exc_type", [
    (None, arguments_exception),
    (123, arguments_exception),
    ([], arguments_exception),
    (True, arguments_exception),
    ("", len_exception),
    ("1" * 19, len_exception),
    ("1" * 21, len_exception),
    ("4070281090000000000a", validation_exception),
    ("4070-810900000000000", validation_exception),
    ("1" * 20, validation_exception),
    ("99999999999999999999", validation_exception),
])
def test_invalid_result_organization_model_account(value, exc_type):
    """
    Проверяет все сценарии невалидного счёта.
    """
    with pytest.raises(exc_type):
        _make_organization(account=value)


@pytest.mark.parametrize("value, exc_type", [
    (None, arguments_exception),
    (123, arguments_exception),
    ([], arguments_exception),
    (True, arguments_exception),
    ("А" * 51, max_len_exception),
])
def test_invalid_result_organization_model_owner(value, exc_type):
    """
    Проверяет невалидные значения owner.
    """
    with pytest.raises(exc_type):
        _make_organization(owner=value)


def test_valid_result_organization_model_owner_correct():
    """
    Проверяет, что корректный owner принимается без исключений.
    """
    org = _make_organization(owner=VALID_OWNER)
    assert org.owner == VALID_OWNER
