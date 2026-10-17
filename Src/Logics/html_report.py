from html import escape

from Src.Core.abstract_report import abstract_report
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Logics.report_utils import extract_table


class html_report(abstract_report):
    def build(self, source):
        validator.validate(source, abstract_model)
        headers, rows = extract_table(source)

        lines = ['<table border="1">', "<tr>"]
        for header in headers:
            lines.append(f"<th>{escape(str(header))}</th>")
        lines.append("</tr>")
        for row in rows:
            lines.append("<tr>")
            for cell in row:
                lines.append(f"<td>{escape(str(cell))}</td>")
            lines.append("</tr>")
        lines.append("</table>")

        result = report_result_model()
        result.text = "\n".join(lines)
        return result
