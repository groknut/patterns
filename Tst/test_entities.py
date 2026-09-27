# Необходимо установить pip install pytest в терминале с подключенным Environment
# Далее, настройки
# {
   # "python.testing.pytestArgs": [
   #     "Tst"
   # ],
   # "python.testing.unittestEnabled": false,
   # "python.testing.pytestEnabled": true
#}

from Src.Core.entity_model import entity
from Src.Core.exception import arguments_exception, max_length_exception
import pytest

class test_entity(entity):
    """Тестовая сущность"""
    pass

# Пример простого теста
def test_start():
    assert 1 == 1

def test_abstract_model_get_id_not_null():
    """entity id not equals null"""
    entity_model = test_entity()
    result = entity_model.id
    assert result != ""


def test_unique_entity():
    """2 модели имеют уникальные id"""
    entity_model_1 = test_entity()
    entity_model_2 = test_entity()
    assert entity_model_1.id != entity_model_2.id

def test_argument_exception_witn_empty_name():
    """Тест ошибки на пустое имя"""
    entity = test_entity()
    empty_name = ""

    with pytest.raises(arguments_exception) as exception:
        entity.name = empty_name

    assert "Wrong argument: name" == exception.value.message

def test_max_length_exception_with_set_name():
    """Тест ошибки на имя больше 50 символов"""
    entity = test_entity()
    new_name = "a"*51
    with pytest.raises(max_length_exception) as exception:
        entity.name = new_name

    assert "Max length (50)" == exception.value.message

def test_private_fields_not_visible():
    """__id, __name не доступны"""
    entity_model = test_entity()
    assert not hasattr(entity_model, "__id")
    assert not hasattr(entity_model, "__name")
