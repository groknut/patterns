from Src.Core.abstract_report import abstract_report
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Logics.report_utils import extract_table


class text_report(abstract_report):
    def build(self, source):
        validator.validate(source, abstract_model)
        headers, rows = extract_table(source)

        lines = [" | ".join(headers)]
        for row in rows:
            lines.append(" | ".join(str(cell) for cell in row))

        result = report_result_model()
        result.text = "\n".join(lines)
        return result
