from abc import ABC, abstractmethod


class abstract_balance_prototype(ABC):
    """Прототип формирования оборотно-сальдовой ведомости."""

    @abstractmethod
    def build_balance(self, objects: list) -> list[dict]:
        """Построить ОСВ по списку объектов."""
        ...
