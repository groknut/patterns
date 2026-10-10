from Src.Logics.settings_manager import settings_manager
from Src.Core.validator import argument_exception


def test_no_raise_settings_manager_load():
    manager = settings_manager()
    try:
        manager.load()
        assert True
    except argument_exception:
        assert False


def test_not_empty_settings_manager_load():
    # проверить загрузку настроек. они не пусты
    manager = settings_manager()
    try:
        manager.load()
        assert True
    except:
        assert False
    assert manager.settings is not None


def test_equals_settings_manager_create():
    instance_1 = settings_manager()
    instance_2 = settings_manager()

    assert instance_1 == instance_2


def test_is_loaded_settings_manager_true():
    manager = settings_manager()
    try:
        manager.load()
    except argument_exception:
        assert False
    assert manager.is_loaded


def test_equals_settings_from_settings_managers():
    instance_1 = settings_manager()
    instance_2 = settings_manager()

    assert instance_1.settings == instance_2.settings


def test_convert_invalid_data_returns_false():
    """convert() с битым __data возвращает False, а не падает."""
    manager = settings_manager()
    manager._settings_manager__data = {"organization": "not_a_dict"}
    assert manager.convert() is False
