import csv
import io

from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Models.recipe_model import recipe_model


class csv_report(abstract_report):
    __recipe: recipe_model

    def build(self, source):
        validator.validate(source, recipe_model)
        self.__recipe = source

        buffer = io.StringIO()
        writer = csv.writer(buffer, delimiter=";", lineterminator="\n")
        writer.writerow(["Код", "Наименование", "Брутто", "Нетто"])
        for item in self.__recipe.ingredients:
            writer.writerow(
                [item.id, item.name, item.gross_weight, item.net_weight]
            )

        payload = buffer.getvalue().encode("utf-8")

        result = report_result_model()
        result.binary = list(payload)
        return result
