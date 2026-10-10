from collections.abc import Iterable

from Src.Core.entity_model import entity_model
from Src.Core.validator import validator, argument_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model  # <-- из своего модуля


class recipe_model(entity_model):
    """Технологическая карта (рецепт) одной номенклатуры-результата."""

    __result: nomenclature_model = None
    __output_quantity: float = 1.0
    __cooking_time_minutes: float = 1.0
    __steps: list = None
    __ingredients: dict = None

    def __init__(
        self,
        name: str = "",
        result: nomenclature_model = None,
        output_quantity: float = 1.0,
        cooking_time_minutes: float = 1.0,
        steps: Iterable = (),
        ingredients: Iterable = (),
    ) -> None:
        super().__init__()
        self.name = name
        if result is not None:
            validator.validate(result, nomenclature_model)
            self.__result = result
        self.output_quantity = output_quantity
        self.cooking_time_minutes = cooking_time_minutes
        self.steps = steps
        self.__ingredients = {}
        for ing in ingredients:
            self.add_ingredient(ing)

    @property
    def result(self) -> nomenclature_model:
        return self.__result

    @property
    def output_quantity(self) -> float:
        return self.__output_quantity

    @output_quantity.setter
    def output_quantity(self, value) -> None:
        validator.validate(value, (int, float))
        if value <= 0:
            raise argument_exception("Выход должен быть больше нуля")
        self.__output_quantity = float(value)

    @property
    def cooking_time_minutes(self) -> float:
        return self.__cooking_time_minutes

    @cooking_time_minutes.setter
    def cooking_time_minutes(self, value) -> None:
        validator.validate(value, (int, float))
        if value <= 0:
            raise argument_exception("Время должно быть больше нуля")
        self.__cooking_time_minutes = float(value)

    @property
    def steps(self) -> list:
        return list(self.__steps)

    @steps.setter
    def steps(self, value) -> None:
        validator.validate(value, (list, tuple))
        if len(value) == 0:
            raise argument_exception("Список шагов не может быть пустым")
        cleaned = []
        for step in value:
            validator.validate(step, str, 500)
            cleaned.append(step.strip())
        self.__steps = cleaned

    @property
    def ingredients(self) -> list:
        return list(self.__ingredients.values())

    def add_ingredient(self, ingredient: ingredient_model) -> None:
        validator.validate(ingredient, ingredient_model)
        if self.__result is not None and ingredient.nomenclature == self.__result:
            raise argument_exception("Результат карты не может быть её ингредиентом")
        key = ingredient.nomenclature.id
        if key in self.__ingredients:
            raise argument_exception(
                f"Номенклатура «{ingredient.nomenclature.name}» уже есть в составе"
            )
        self.__ingredients[key] = ingredient

    def remove_ingredient(self, nomenclature: nomenclature_model) -> None:
        validator.validate(nomenclature, nomenclature_model)
        if nomenclature.id not in self.__ingredients:
            raise argument_exception("Такой номенклатуры нет в составе")
        del self.__ingredients[nomenclature.id]

    @property
    def gross_weight(self) -> float:
        return sum((i.gross_weight for i in self.__ingredients.values()), 0.0)

    @property
    def net_weight(self) -> float:
        return sum((i.net_weight for i in self.__ingredients.values()), 0.0)

    @staticmethod
    def create_pancakes_recipe(nomenclatures: dict) -> "recipe_model":
        """Фабричный метод: «Оладьи пышные на кефире» на 1 порцию.

        :param nomenclatures: Словарь номенклатуры {id: nomenclature_model}.
        :raises argument_exception: Если в словаре нет нужной номенклатуры.
        """
        by_name = {n.name: n for n in nomenclatures.values()}

        def find(name: str) -> nomenclature_model:
            nom = by_name.get(name)
            if nom is None:
                raise argument_exception(f"Нет номенклатуры «{name}»")
            return nom

        def ing(
            name, quantity, loss_ratio=0.0, grams_per_unit=None
        ) -> ingredient_model:
            nom = find(name)
            return ingredient_model(
                nomenclature=nom,
                range_=nom.range,
                quantity=quantity,
                loss_ratio=loss_ratio,
                grams_per_unit=grams_per_unit,
            )

        return recipe_model(
            name="Оладьи пышные на кефире (1 порция)",
            result=find("Порция оладий пышных на кефире"),
            output_quantity=1,
            cooking_time_minutes=30,
            steps=[
                "Подготовка сырья: муку просеять, масло растопить до 40 °C, "
                "яйца промыть, кефир подогреть до 22 °C.",
                "Замес: взбить яйца с сахарной пудрой и содой, влить тёплый кефир, "
                "ввести муку порциями, добавить растопленное масло. "
                "Дать тесту отдохнуть 10–15 минут.",
                "Выпекание: сковороду разогреть до 170–190 °C, выкладывать тесто "
                "по 40–50 г, обжарить 2–3 минуты с одной стороны и "
                "1,5–2 минуты с другой до золотистой корочки.",
            ],
            ingredients=[
                ing("Мука ржаная", 0.0625, loss_ratio=0.02),  # 62,5 г
                ing("Кефир 1%", 100, loss_ratio=0.05),  # 100 мл
                ing(
                    "Яйца перепелиные", 2, loss_ratio=0.10, grams_per_unit=10.0
                ),  # 2 шт × 10 г
                ing("Масло топлёное", 0.01, loss_ratio=0.15),  # 10 г
                ing("Сахарная пудра", 0.01),  # 10 г
                ing("Сода пищевая", 0.001),  # 1 г
            ],
        )
