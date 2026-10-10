from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator, argument_exception
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.storage_model import storage_model
from Src.Models.recipe_model import recipe_model


class storage_manager(abstract_manager):
    """Менеджер хранения доменных моделей.
    При первом старте формируются первичные значения через фабричные методы моделей.
    """

    __ranges: dict = None
    __storages: dict = None
    __nomenclatures: dict = None
    __groups: dict = None
    __recipes: dict = None
    __is_initialized: bool = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
            obj = super(storage_manager, cls).__new__(cls)
            obj.__ranges = {}
            obj.__storages = {}
            obj.__nomenclatures = {}
            obj.__groups = {}
            obj.__recipes = {}
            obj.__is_initialized = False
            cls.instance = obj
        return cls.instance

    def convert(self, is_first: bool) -> bool:
        if not is_first:
            return True
        if self.__is_initialized:
            return True
        try:
            self.__initialize_primary_data()
            return True
        except argument_exception:
            return False

    def __initialize_primary_data(self) -> None:
        self.__create_ranges()
        self.__create_groups()
        self.__create_nomenclatures()
        self.__create_storages()
        self.__create_recipes()
        self.__is_initialized = True

    def __create_ranges(self) -> None:
        """
        Единицы измерения — через фабрики range_model
        """
        for rng in (
            range_model.create_gramm(),
            range_model.create_kilogram(),
            range_model.create_liter(),
            range_model.create_milliliter(),
            range_model.create_piece(),
        ):
            self.add_object(range_model, self.__ranges, rng)

    def __create_groups(self) -> None:
        """
        Группы — через фабрики group_model
        """
        for grp in (
            group_model.create_grocery(),
            group_model.create_dairy(),
            group_model.create_dishes(),
            group_model.create_packaging(),
        ):
            self.add_object(group_model, self.__groups, grp)

    def __create_nomenclatures(self) -> None:
        """
        Номенклатура — через фабрики nomenclature_model
        """
        groups = {g.name: g for g in self.__groups.values()}
        ranges = {r.name: r for r in self.__ranges.values()}

        grocery = groups.get("Бакалея")
        dairy = groups.get("Молочные продукты")
        dishes = groups.get("Блюда")
        packaging = groups.get("Упаковка")

        kg = ranges.get("килограмм")
        ml = ranges.get("миллилитр")
        piece = ranges.get("штука")

        items = (
            nomenclature_model.create_ingredient(
                "Мука ржаная", "Мука ржаная обдирная", grocery, kg
            ),
            nomenclature_model.create_ingredient(
                "Кефир 1%", "Кефир коровий пастеризованный 1%", dairy, ml
            ),
            nomenclature_model.create_ingredient(
                "Яйца перепелиные", "Яйца перепелиные столовые", dairy, piece
            ),
            nomenclature_model.create_ingredient(
                "Масло топлёное", "Масло топлёное ГОСТ 72.5%", dairy, kg
            ),
            nomenclature_model.create_ingredient(
                "Сахарная пудра", "Сахарная пудра М50", grocery, kg
            ),
            nomenclature_model.create_ingredient(
                "Сода пищевая", "Сода пищевая двууглекислая", grocery, kg
            ),
            nomenclature_model.create_pancake_portion(dishes, piece),
            nomenclature_model.create_ingredient(
                "Плёнка пищевая", "Плёнка пищевая ПВХ 300 мм", packaging, piece
            ),
            nomenclature_model.create_ingredient(
                "Упаковка оладий", "Оладьи пышные, упакованные", dishes, piece
            ),
        )
        for item in items:
            self.add_object(nomenclature_model, self.__nomenclatures, item)

    def __create_storages(self) -> None:
        """
        Склады — через фабрики storage_model
        """
        for storage in (storage_model.create_main(), storage_model.create_fridge()):
            self.add_object(storage_model, self.__storages, storage)

    def __create_recipes(self) -> None:
        """Рецепт — через фабрику recipe_model"""
        for recipe in (
            recipe_model.create_pancakes_recipe(self.__nomenclatures),
            recipe_model.create_packed_pancakes_recipe(self.__nomenclatures),
        ):
            self.add_object(recipe_model, self.__recipes, recipe)

    def add_object(self, type_, group, item) -> bool:
        """Общий метод добвления"""
        try:
            validator.validate(item, type_)
            if item.id in group:
                return False
            group[item.id] = item
            return True
        except argument_exception:
            return False

    # ------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------
    @property
    def ranges(self) -> dict:
        return self.__ranges

    @property
    def storages(self) -> dict:
        return self.__storages

    @property
    def groups(self) -> dict:
        return self.__groups

    @property
    def nomenclatures(self) -> dict:
        return self.__nomenclatures

    @property
    def recipes(self) -> dict:
        return self.__recipes

    @property
    def data(self) -> dict:
        return {
            "storages": self.__storages,
            "ranges": self.__ranges,
            "nomenclatures": self.__nomenclatures,
            "groups": self.__groups,
            "recipes": self.__recipes,
        }

    @property
    def is_initialized(self) -> bool:
        return self.__is_initialized


    # Ревью:
    # Нет. Не верно. Нужен рекурсивный подход. Не реализован вариант "блюдо в блюде"
    def get_recipe_by_result(self, nomenclature: nomenclature_model):
        """Карта, результатом которой является указанная номенклатура, или None."""
        for r in self.__recipes.values():
            if r.result == nomenclature:
                return r
        return None

    def get_gross_weight(self, recipe: recipe_model, seen: list = None) -> float:
        """Полный вес Брутто с раскрытием полуфабрикатов."""
        seen = seen or []
        if recipe.id in seen:
            return 0.0
        seen = seen + [recipe.id]

        total = 0.0
        for ing in recipe.ingredients:
            nested = self.get_recipe_by_result(ing.nomenclature)
            if nested is not None:
                scale = ing.quantity / nested.output_quantity
                total += self.get_gross_weight(nested, seen) * scale
            else:
                total += ing.gross_weight
        return total

    def get_net_weight(self, recipe: recipe_model, seen: list = None) -> float:
        """Полный вес Нетто с раскрытием полуфабрикатов."""
        seen = seen or []
        if recipe.id in seen:
            return 0.0
        seen = seen + [recipe.id]

        total = 0.0
        for ing in recipe.ingredients:
            nested = self.get_recipe_by_result(ing.nomenclature)
            if nested is not None:
                scale = ing.quantity / nested.output_quantity
                total += self.get_net_weight(nested, seen) * scale
            else:
                total += ing.net_weight
        return total
