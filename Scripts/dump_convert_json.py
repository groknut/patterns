import json
from pathlib import Path

from Src.Dtos.report_type_dto import entity_type_enum
from Src.Logics.convert_factory import convert_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager

OUTPUT_DIR = Path("Docs/JsonExamples")
factory = convert_factory()

def dump(name: str, data: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{name}.json"
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  → {path}")


def main() -> None:
    settings_manager().load()
    storage_manager().convert(True)

    for etype, collection in (
        (entity_type_enum.NOMENCLATURE, storage_manager().nomenclatures),
        (entity_type_enum.RANGE, storage_manager().ranges),
        (entity_type_enum.RECIPE, storage_manager().recipes),
    ):
        for code, entity in collection.items():
            dump(f"{etype.value}_{code[:8]}", factory.convert(entity))


if __name__ == "__main__":
    main()
