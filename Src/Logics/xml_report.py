from xml.etree.ElementTree import Element, SubElement, tostring

from Src.Core.abstract_report import abstract_report
from Src.Core.report_source import report_source
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model


class xml_report(abstract_report):

    @property
    def is_binary(self) -> bool:
        return False

    @property
    def media_type(self) -> str:
        return "application/xml; charset=utf-8"

    @property
    def file_extension(self) -> str:
        return "xml"

    def build(self, source):
        validator.validate(source, report_source)

        headers = source.report_headers()
        root = Element("report")
        root.set("entity", type(source).__name__)
        for row in source.report_rows():
            row_el = SubElement(root, "row")
            for header, cell in zip(headers, row):
                column = SubElement(row_el, "column")
                column.set("name", header)
                column.text = str(cell)

        result = report_result_model()
        result.text = tostring(root, encoding="unicode")
        return result
