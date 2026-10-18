from Src.Core.abstract_report import abstract_report
from Src.Core.reportable import reportable
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model


class text_report(abstract_report):
    @property
    def is_binary(self) -> bool:
        return False

    @property
    def media_type(self) -> str:
        return "text/plain; charset=utf-8"

    @property
    def file_extension(self) -> str:
        return "txt"

    def build(self, source):
        validator.validate(source, reportable)

        lines = [" | ".join(source.report_headers())]
        for row in source.report_rows():
            lines.append(" | ".join(str(cell) for cell in row))

        result = report_result_model()
        result.text = "\n".join(lines)
        return result
