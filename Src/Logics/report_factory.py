from Src.Core.abstract_factory import abstract_report_factory
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import argument_exception, validator
from Src.Dtos.report_type_dto import report_type_enum
from Src.Logics.csv_report import csv_report
from Src.Logics.html_report import html_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.settings_manager import settings_manager
from Src.Logics.text_report import text_report
from Src.Logics.xml_report import xml_report


class report_factory(abstract_report_factory):
    """Реализация фабрики для построения отчетов"""

    # маппинг типа отчета и его реализации
    __mapping: dict

    # менеджер настроек
    __settings_manager: settings_manager

    def __init__(self):
        self.__mapping = {
            report_type_enum.TXT: text_report,
            report_type_enum.CSV: csv_report,
            report_type_enum.MARKDOWN: markdown_report,
            report_type_enum.XML: xml_report,
            report_type_enum.HTML: html_report,
        }
        self.__settings_manager = settings_manager()

    def create(self, report_type) -> abstract_report:
        """Создать отчет указанного формата.
        Принимает как член `report_type_enum`, так и строку
        """
        validator.validate(report_type, report_type_enum)
        report_type = report_type_enum.from_str(report_type)

        if report_type not in self.__mapping:
            raise argument_exception(
                f"Указанный тип отчета {report_type} не реализован"
            )
        return self.__mapping[report_type]()

    def create_default(self) -> abstract_report:
        """Создать отчет в формате из настроек (settings_model.response_format)."""
        settings = self.__settings_manager.settings
        fmt = settings.response_format if settings is not None else report_type_enum.TXT
        return self.create(fmt)
