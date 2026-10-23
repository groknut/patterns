from datetime import date, datetime

from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor


def test_wrap_value_basic_convertor_for_int():
    """basic_convertor(42) → {"value": 42}"""
    assert basic_convertor().convert(42) == {"value": 42}


def test_wrap_value_basic_convertor_for_str():
    """basic_convertor("ООО Ромашка") → {"value": "ООО Ромашка"}"""
    assert basic_convertor().convert("ООО Ромашка") == {"value": "ООО Ромашка"}

def test_wrap_value_datetime_convertor_for_datetime():
    """datetime_convertor(datetime) → {"iso": "2024-01-15T10:30:00"}"""
    dt = datetime(2024, 1, 15, 10, 30, 0)
    assert datetime_convertor().convert(dt) == {"iso": "2024-01-15T10:30:00"}


def test_wrap_value_datetime_convertor_for_date():
    """datetime_convertor(date) → {"iso": "2024-01-15"}"""
    d = date(2024, 1, 15)
    assert datetime_convertor().convert(d) == {"iso": "2024-01-15"}
