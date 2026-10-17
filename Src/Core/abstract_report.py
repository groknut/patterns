from abc import ABC, abstractmethod

from Src.Core.abstract_model import abstract_model
from Src.Dtos.abstract_result_model import report_result_model


class abstract_report(ABC):
    """Формировать отчет"""

    @abstractmethod
    def build(self, source: abstract_model) -> report_result_model:
        pass
