from Src.Core.abstract_report import abstract_report
from Src.Core.reportable import reportable
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model


class markdown_report(abstract_report):

    @property
    def is_binary(self) -> bool:
        return True

    @property
    def media_type(self) -> str:
        return "text/markdown; charset=utf-8"

    @property
    def file_extension(self) -> str:
        return "md"

    def build(self, source):
        validator.validate(source, reportable)

        headers = source.report_headers()
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("| " + " | ".join("---" for _ in headers) + " |")
        for row in source.report_rows():
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

        payload = "\n".join(lines).encode("utf-8")

        result = report_result_model()
        result.binary = list(payload)
        return result
