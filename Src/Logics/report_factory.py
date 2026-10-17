from Src.Core.abstract_factory import abstract_report_factory
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import report_type_enum
from Src.Logics.text_report import text_report


class report_factory(abstract_report_factory):
    """Реализация фабрики для построения отчетов"""

    # маппинг типа отчета и его реализации
    __mapping = dict[report_type_enum, abstract_report]

    def __init__(self):
        self.__mapping[report_type_enum.TXT] = text_report

    def create(self, report_type: report_type_enum) -> abstract_report:
        if report_type not in self.__mapping.keys:
            raise argument_exception(
                f"Указанный тип отчета {report_type} не реализован"
            )
        return self.__mapping[report_type]
