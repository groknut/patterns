import csv
import io

from Src.Core.abstract_report import abstract_report
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Logics.report_utils import extract_table


class csv_report(abstract_report):
    def build(self, source):
        validator.validate(source, abstract_model)
        headers, rows = extract_table(source)

        buffer = io.StringIO()
        writer = csv.writer(buffer, delimiter=";", lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)
        payload = buffer.getvalue().encode("utf-8")

        result = report_result_model()
        result.binary = list(payload)
        return result
