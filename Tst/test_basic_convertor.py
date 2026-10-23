from Src.Logics.basic_convertor import basic_convertor


def test_wrap_value_basic_convertor_for_int():
    """basic_convertor(42) → {"value": 42}"""
    assert basic_convertor().convert(42) == {"value": 42}


def test_wrap_value_basic_convertor_for_str():
    """basic_convertor("ООО Ромашка") → {"value": "ООО Ромашка"}"""
    assert basic_convertor().convert("ООО Ромашка") == {"value": "ООО Ромашка"}
