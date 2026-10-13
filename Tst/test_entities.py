# Необходимо установить pip install pytest в терминале с подключенным Environment
# Далее, настройки
# {
# "python.testing.pytestArgs": [
#     "Tst"
# ],
# "python.testing.unittestEnabled": false,
# "python.testing.pytestEnabled": true
# }

from Src.Core.entity_model import entity_model
from Src.Core.validator import argument_exception
import pytest


class test_entity(entity_model):
    """Тестовая сущность"""

    pass


# Пример простого теста
def test_start():
    assert 1 == 1


def test_abstract_model_get_id_not_null():
    """entity_model id not equals null"""
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
    entity_model = test_entity()
    empty_name = ""

    with pytest.raises(argument_exception) as exception:
        entity_model.name = empty_name


def test_max_len_exception_with_set_name():
    """Тест ошибки на имя больше 50 символов"""
    entity_model = test_entity()
    new_name = "a" * 51
    with pytest.raises(argument_exception) as exception:
        entity_model.name = new_name


def test_private_fields_not_visible():
    """__id, __name не доступны"""
    entity_model = test_entity()
    assert not hasattr(entity_model, "__id")
    assert not hasattr(entity_model, "__name")
