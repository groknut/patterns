from html import escape

from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Models.recipe_model import recipe_model


class html_report(abstract_report):
    __recipe: recipe_model

    def build(self, source):
        validator.validate(source, recipe_model)
        self.__recipe = source

        lines = ['<table border="1">']
        lines.append(
            "<tr><th>Код</th><th>Наименование</th>"
            "<th>Брутто</th><th>Нетто</th></tr>"
        )
        for item in self.__recipe.ingredients:
            lines.append(
                f"<tr><td>{escape(item.id)}</td>"
                f"<td>{escape(item.name)}</td>"
                f"<td>{item.gross_weight}</td>"
                f"<td>{item.net_weight}</td></tr>"
            )
        lines.append("</table>")

        result = report_result_model()
        result.text = "\n".join(lines)
        return result
