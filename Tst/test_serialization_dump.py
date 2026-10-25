import json
from pathlib import Path

from Src.Logics.convert_factory import convert_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager


def test_dump_storage_to_single_json():
    """Выгружает все данные storage_manager в один файл Docs/JsonExamples/storage_dump.json"""
    settings_manager().load()
    storage_manager().convert(True)
    factory = convert_factory()

    data = {
        "nomenclatures": [
            factory.convert(x)
            for x in storage_manager().nomenclatures.values()
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
        json.dump(data, f, ensure_ascii=False, indent=2)

    assert path.exists()
    assert path.stat().st_size > 0
