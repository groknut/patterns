import json
from pathlib import Path

from Src.Logics.convert_factory import convert_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model

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

def test_dump_and_load_storage():
    """Выгружает данные в JSON, загружает обратно, десериализует и сравнивает"""

    settings_manager().load()
    storage_manager().convert(True)
    factory = convert_factory()

    original_data = {
        "nomenclatures": [
            factory.convert(x) for x in storage_manager().nomenclatures.values()
        ],
        "ranges": [
            factory.convert(x) for x in storage_manager().ranges.values()
        ],
        "recipes": [
            factory.convert(x) for x in storage_manager().recipes.values()
        ],
    }

    out_dir = Path("Docs/JsonExamples")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "storage_dump.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(original_data, f, ensure_ascii=False, indent=2)

    with open(path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    # Сравниваем Номенклатуру
    for orig_dict in loaded_data["nomenclatures"]:
        restored_model = factory.deserialize(orig_dict, nomenclature_model)
        restored_dict = factory.convert(restored_model)
        assert restored_dict == orig_dict, f"Ошибка номенклатуры: {orig_dict.get('name')}"

    # Сравниваем Единицы измерения (рекурсия base)
    for orig_dict in loaded_data["ranges"]:
        restored_model = factory.deserialize(orig_dict, range_model)
        restored_dict = factory.convert(restored_model)
        assert restored_dict == orig_dict, f"Ошибка единицы: {orig_dict.get('name')}"

    # Сравниваем Рецепты (списки ингредиентов и шагов)
    for orig_dict in loaded_data["recipes"]:
        restored_model = factory.deserialize(orig_dict, recipe_model)
        restored_dict = factory.convert(restored_model)
        assert restored_dict == orig_dict, f"Ошибка рецепта: {orig_dict.get('name')}"

        assert len(restored_model.ingredients) > 0
        assert len(restored_model.steps) > 0
