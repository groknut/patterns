from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class EntityReference:
    """Ссылка из одной доменной сущности на другую."""
    entity_type: str
    entity_id: str
    entity_name: str
    field: str

    def to_dict(self) -> dict:
        """Сериализация для JSON-ответа."""
        return asdict(self)
