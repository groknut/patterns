
from Src.Models.warehouse_model import warehouse_model
from Src.Core.exception import arguments_exception, max_len_exception
import pytest

class test_entity(warehouse_model):
    """Тестовая сущность"""
    pass

def test_max_len_exception_with_set_address():
    """Тест ошибки на адрес больше 255 символов"""
    entity = test_entity()
    address = "a"*256
    with pytest.raises(max_len_exception) as exception:
        entity.address = address

    assert "Max length (255)" == exception.value.message
