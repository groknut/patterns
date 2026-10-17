from xml.etree.ElementTree import Element, SubElement, tostring

from Src.Core.abstract_report import abstract_report
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Logics.report_utils import extract_table


class xml_report(abstract_report):
    def build(self, source):
        validator.validate(source, abstract_model)
        headers, rows = extract_table(source)

        root = Element("report")
        root.set("entity", type(source).__name__)
        for row in rows:
            row_el = SubElement(root, "row")
            for header, cell in zip(headers, row):
                column = SubElement(row_el, "column")
                column.set("name", header)
                column.text = str(cell)

        result = report_result_model()
        result.text = tostring(root, encoding="unicode")
        return result
