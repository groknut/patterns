from collections import defaultdict
from datetime import date

from Src.Dtos.balance_dto import balance_dto
from Src.Dtos.filter_condition_enum import filter_condition_enum
from Src.Dtos.filter_dto import filter_dto
from Src.Logics.prototypes import filter_prototype
from Src.Models.movement_model import movement_model, movement_operation_enum


class balance_service:
    """Сервис формирования ОСВ.
    Использует filter_prototype для отбора, затем вычисляет движения
    и формирует balance_dto для сериализации.
    """

    def build(
           self,
           movements: list[movement_model],
           dto: filter_dto | None,
           start_date: date,
           end_date: date,
    ) -> list[balance_dto]:

           # Базовый прототип + пользовательский фильтр (например, по name)
           base = filter_prototype(movements)
           if dto is not None:
               base = base.filter(dto)

           # 1. Начальные остатки (date <= start_date)
           opening_movements = base.filter(filter_dto(
               field="date", value=start_date.isoformat(),
               condition=filter_condition_enum.LESS_OR_EQUAL,
           )).data

           # 2. Обороты периода (start_date <= date <= end_date)
           period_movements = base.filter(filter_dto(
               field="date", value=start_date.isoformat(),
               condition=filter_condition_enum.GREATER_OR_EQUAL,
           )).filter(filter_dto(
               field="date", value=end_date.isoformat(),
               condition=filter_condition_enum.LESS_OR_EQUAL,
           )).data

           # 3. Агрегация
           opening = self.__aggregate_balance(opening_movements)
           turnover = self.__aggregate_turnover(period_movements)

           # 4. Склейка + DTO
           nom_map = {}
           for m in movements:
               if m.nomenclature is not None:
                   nom_map[m.nomenclature.id] = m.nomenclature

           result: list[balance_dto] = []
           for nom_id in set(opening) | set(turnover):
               ob = opening.get(nom_id, 0.0)
               inc = turnover.get(nom_id, {}).get("income", 0.0)
               exp = turnover.get(nom_id, {}).get("expense", 0.0)
               nom = nom_map.get(nom_id)

               result.append(balance_dto(
                   id=nom_id,
                   name=getattr(nom, "name", "") if nom else "",
                   unit=getattr(nom.range, "name", "") if nom and nom.range else "",
                   opening_balance=ob,
                   income=inc,
                   expense=exp,
                   closing_balance=ob + inc - exp,
               ))
           return result

    @staticmethod
    def __aggregate_balance(movements: list) -> dict[str, float]:
        """Начальный остаток: приход - расход."""
        bal: dict[str, float] = defaultdict(float)
        for m in movements:
            if m.nomenclature is None:
                continue
            nid = m.nomenclature.id
            if m.operation == movement_operation_enum.INCOME:
                bal[nid] += m.quantity
            else:
                bal[nid] -= m.quantity
        return dict(bal)

    @staticmethod
    def __aggregate_turnover(movements: list) -> dict[str, dict[str, float]]:
        """Обороты: {nom_id: {income, expense}}."""
        t: dict[str, dict[str, float]] = defaultdict(
            lambda: {"income": 0.0, "expense": 0.0}
        )
        for m in movements:
            if m.nomenclature is None:
                continue
            nid = m.nomenclature.id
            if m.operation == movement_operation_enum.INCOME:
                t[nid]["income"] += m.quantity
            else:
                t[nid]["expense"] += m.quantity
        return dict(t)
