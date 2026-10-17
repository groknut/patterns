from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Logics.storage_manager import storage_manager
from Src.Models.recipe_model import recipe_model


class text_report(abstract_report):
    __recipe: recipe_model

    def build(self, source):
        validator.validate(source, recipe_model)
        self.__recipe = source

        header = "Код | Наименование | Брутто | Нетто"

        data = []

        for item in self.__recipe.ingredients:
            data.append(
                f"{item.id} | {item.name} | {item.gross_weight} {item.net_weight}"
            )

        result = report_result_model()
        result.text = "\n".join(data)
        return result
