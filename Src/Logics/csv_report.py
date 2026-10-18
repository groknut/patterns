import csv
import io

from Src.Core.abstract_report import abstract_report
from Src.Core.reportable import reportable
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model


class csv_report(abstract_report):

    @property
    def is_binary(self) -> bool:
        return True

    @property
    def media_type(self) -> str:
        return "text/csv; charset=utf-8"

    @property
    def file_extension(self) -> str:
        return "csv"

    def build(self, source):
        validator.validate(source, reportable)

        buffer = io.StringIO()
        writer = csv.writer(buffer, delimiter=";", lineterminator="\n")
        writer.writerow(source.report_headers())
        writer.writerows(source.report_rows())
        payload = buffer.getvalue().encode("utf-8")

        result = report_result_model()
        result.binary = list(payload)
        return result
