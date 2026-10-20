import pytest

from Src.Core.validator import argument_exception
from Src.Models.storage_model import storage_model


class test_entity(storage_model):
    """Тестовая сущность"""


def test_max_len_exception_with_set_address():
    """Тест ошибки на адрес больше 255 символов"""
    entity_model = test_entity()
    address = "a" * 256
    with pytest.raises(argument_exception):
        entity_model.address = address
