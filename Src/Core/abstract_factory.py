from abc import ABC, abstractmethod

from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_type_dto import report_type_enum


class abstract_report_factory(ABC):
    """Фабрика отчета"""

    @abstractmethod
    def create(self, report_type: report_type_enum) -> abstract_report:
        """Создает отчет указанного формата."""
        pass

    @abstractmethod
    def create_default(self) -> abstract_report:
        """Создает отчет в формате из настроек приложения."""
        pass
