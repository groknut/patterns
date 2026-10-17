from xml.etree.ElementTree import Element, SubElement, tostring

from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator
from Src.Dtos.abstract_result_model import report_result_model
from Src.Models.recipe_model import recipe_model


class xml_report(abstract_report):
    __recipe: recipe_model

    def build(self, source):
        validator.validate(source, recipe_model)
        self.__recipe = source

        root = Element("recipe")
        for item in self.__recipe.ingredients:
            row = SubElement(root, "ingredient")
            SubElement(row, "code").text = item.id
            SubElement(row, "name").text = item.name
            SubElement(row, "gross").text = str(item.gross_weight)
            SubElement(row, "net").text = str(item.net_weight)

        result = report_result_model()
        result.text = tostring(root, encoding="unicode")
        return result
