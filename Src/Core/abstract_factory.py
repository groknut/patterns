from abc import ABC, abstractmethod

from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_type_dto import report_type_enum


class abstract_report_factory(ABC):
    """Фабрика отчета"""

    def create(report_type: report_type_enum):
        pass
