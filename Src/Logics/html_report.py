from html import escape

from Src.Core.abstract_report import abstract_report
from Src.Core.reportable import reportable
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model


class html_report(abstract_report):

    @property
    def is_binary(self) -> bool:
        return False

    @property
    def media_type(self) -> str:
        return "text/html; charset=utf-8"

    @property
    def file_extension(self) -> str:
        return "html"

    def build(self, source):
        validator.validate(source, reportable)

        headers = source.report_headers()
        lines = ['<table border="1"><tr>']
        lines += [f"<th>{escape(str(h))}</th>" for h in headers]
        lines.append("</tr>")
        for row in source.report_rows():
            lines.append("<tr>")
            lines += [f"<td>{escape(str(cell))}</td>" for cell in row]
            lines.append("</tr>")
        lines.append("</table>")

        result = report_result_model()
        result.text = "\n".join(lines)
        return result
