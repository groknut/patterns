from Src.Core.abstract_balance_prototype import abstract_balance_prototype


class balance_prototype(abstract_balance_prototype):
    """Формирует псевдо-ОСВ"""

    def build_balance(self, objects: list) -> list[dict]:
        result = []
        for obj in objects:
            h = sum(ord(c) for c in obj.id)
            opening = h % 100
            income = (h * 2) % 100
            expense = (h * 3) % 100

            result.append({
                "id": obj.id,
                "name": getattr(obj, "name", ""),
                "opening_balance": opening,
                "income": income,
                "expense": expense,
                "closing_balance": opening + income - expense,
            })
        return result
