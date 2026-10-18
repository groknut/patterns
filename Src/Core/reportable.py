from abc import ABC, abstractmethod


class reportable(ABC):
    """Абстракция доменной сущности, способной представить себя в отчёте.
    Отчётные форматы (TXT/CSV/Markdown/XML/HTML) зависят только от этой
    абстракции — конкретные доменные типы им неведомы.
    """

    @abstractmethod
    def report_headers(self) -> list[str]:
        """Заголовки колонок отчёта."""
        pass

    @abstractmethod
    def report_rows(self) -> list[list[str]]:
        """Строки данных отчёта, согласованные с report_headers()."""
        pass
