from Src.Logics.storage_manager import storage_manager
from Src.Core.validator import operation_exception
from Src.Logics.settings_manager import settings_manager
import pytest

@pytest.fixture
def settings_managers():
    """Генерация settings managers для тестов"""
    s1 = settings_manager()
    s2 = settings_manager()
    s1.load()
    s2.load()
    s2.is_first = False
    return s1, s2

def test_equals_storage_manager():
    """Два новых storage_manager должны быть равны"""
    instance1 = storage_manager()
    instance2 = storage_manager()

    assert instance1 == instance2

def test_change_is_first_after_initing_storage_manager(settings_managers):
    """Проверяем смену флаша после генерации"""
    instance1 = storage_manager()
    s = settings_managers[0]
    instance1.convert(s.is_first)
    assert instance1.is_initialized == True


def test_equals_nomenclature_storage_manager():
    """Ед. изм. двух новых storage_manager должны совпадать"""
    instance1 = storage_manager()
    instance2 = storage_manager()
    assert instance1.ranges == instance2.ranges

def test_empty_storage_manager_convert_is_first_start_false(settings_managers):
    """Ожидание: Пустые коллекции при is_first_start == False. Не выполняется, все коллекции остаются пустыми."""
    s2 = settings_managers[1]
    manager = storage_manager()

    if hasattr(storage_manager, "instance"):
        del storage_manager.instance

    try:
        result = manager.convert(s2.is_first)
        assert result == True
        assert len(manager.ranges) == 0
        assert len(manager.groups) == 0
        assert len(manager.nomenclatures) == 0
        assert len(manager.storages) == 0

    finally:
        if hasattr(storage_manager, 'instance'):
            del storage_manager.instance
