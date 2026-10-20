from abc import ABC, abstractmethod


class report_source(ABC):
    """Источник данных для отчёта. Абстракция отчётного контекста."""

    @abstractmethod
    def report_headers(self) -> list[str]: ...

    @abstractmethod
    def report_rows(self) -> list[list[str]]: ...
