from abc import ABC, abstractmethod

from Src.Core.report_source import report_source
from Src.Dtos.abstract_result_model import report_result_model


class abstract_report(ABC):
    """Формировать отчет"""

    @abstractmethod
    def build(self, source: report_source) -> report_result_model:
        pass

    @property
    @abstractmethod
    def is_binary(self) -> bool:
        """True — результат отдаётся как файл, False — как текст."""

    @property
    @abstractmethod
    def media_type(self) -> str:
        """MIME-тип результата."""

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Расширение файла без точки."""
