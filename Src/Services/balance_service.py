from Src.Dtos.balance_dto import balance_dto
from Src.Dtos.filter_dto import filter_dto
from Src.Logics.prototypes import filter_prototype


class balance_service:
    """Сервис формирования ОСВ.
    Использует filter_prototype для отбора, затем вычисляет движения
    и формирует balance_dto для сериализации.
    """

    def build(self, objects: list, dto: filter_dto) -> list[balance_dto]:
        """Сформировать ОСВ по отфильтрованным объектам.

        Шаги:
            1. Натравить filter_prototype на исходные данные → новый прототип
            2. По результату посчитать движения (income, expense)
            3. Сформировать balance_dto для каждой строки
        """

        proto = filter_prototype(objects).filter(dto)
        filtered = proto.data

        result: list[balance_dto] = []
        for obj in filtered:
            h = sum(ord(c) for c in obj.id)
            opening = h % 100
            income = (h * 2) % 100
            expense = (h * 3) % 100
            closing = opening + income - expense

            unit_name = ""
            unit = getattr(obj, "range", None)
            if unit is not None:
                unit_name = getattr(unit, "name", "")

            result.append(
                balance_dto(
                    id=obj.id,
                    name=getattr(obj, "name", ""),
                    unit=unit_name,
                    opening_balance=opening,
                    income=income,
                    expense=expense,
                    closing_balance=closing,
                )
            )
        return result
