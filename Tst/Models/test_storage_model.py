
from Src.Models.storage_model import storage_model
from Src.Core.validator import argument_exception
import pytest

class test_entity(storage_model):
    """Тестовая сущность"""
    pass

def test_max_len_exception_with_set_address():
    """Тест ошибки на адрес больше 255 символов"""
    entity_model = test_entity()
    address = "a"*256
    with pytest.raises(argument_exception) as exception:
        entity_model.address = address
