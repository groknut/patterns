from Src.Logics.convert_factory import convert_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


def test_serialize_deserialize_range_with_recursion():
    """Сериализация/десериализация range_model с рекурсией (base → base)"""
    factory = convert_factory()

    gramm = range_model(name="грамм", coef=1)
    kg = range_model(name="килограмм", coef=1000, base=gramm)

    data = factory.convert(kg)
    restored = factory.deserialize(data, range_model)

    assert restored.name == "килограмм"
    assert restored.base.name == "грамм"
    assert restored.base.base is None


def test_serialize_deserialize_nomenclature_with_links():
    """Сериализация/десериализация nomenclature_model (вложенные group и range)"""
    factory = convert_factory()

    g = group_model(name="Бакалея")
    r = range_model(name="килограмм", coef=1000)
    nom = nomenclature_model(full_name="Мука", name="Мука", group=g, range=r)

    data = factory.convert(nom)
    restored = factory.deserialize(data, nomenclature_model)

    assert restored.id == nom.id
    assert restored.name == "Мука"
    assert restored.group.name == "Бакалея"
    assert restored.range.coef == 1000.0


def test_factory_serialize_and_deserialize_primitives():
    """Фабрика корректно обрабатывает базовые типы и списки"""
    factory = convert_factory()

    # Сериализация
    assert factory.convert(42) == {"value": 42}
    assert factory.convert([1, 2]) == [{"value": 1}, {"value": 2}]

    # Десериализация
    assert factory.deserialize({"value": 42}, int) == 42
    assert factory.deserialize([{"value": 1}, {"value": 2}], list[int]) == [1, 2]

def test_deserialize_from_storage():
    """Берём реальную модель из storage, сериализуем, десериализуем, сравниваем"""
    settings_manager().load()
    storage_manager().convert(True)
    factory = convert_factory()

    original = next(iter(storage_manager().nomenclatures.values()))
    data = factory.convert(original)
    restored = factory.deserialize(data, nomenclature_model)

    assert restored.id == original.id
    assert restored.name == original.name
    assert restored.group.id == original.group.id
    assert restored.range.id == original.range.id
