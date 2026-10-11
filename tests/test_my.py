import pytest
from conftest import load

# Завантажуємо функцію для Варіанта 23 (Задача 8)
M = load(8)

@pytest.mark.parametrize("args, expected_exception, expected_message", [
    (
        ([{"id": "R-01", "owner": "Невідомий", "trigger": {"metric": "m1", "op": ">", "value": 1}}], {"m1": 5}, ["Андрій"], 1),
        ValueError,
        "Ризик R-01: власник Невідомий не входить до команди"
    ),
    (
        ([{"id": "R-02", "owner": "Андрій", "trigger": {"metric": "m1", "op": "!=", "value": 1}}], {"m1": 5}, ["Андрій"], 1),
        ValueError,
        "Ризик R-02: невідома операція «!=»"
    ),
    (
        ([], {"m1": 5}, ["Андрій"], 1),
        ValueError,
        "Реєстр порожній"
    ),
])
def test_my_error_cases(args, expected_exception, expected_message):
    with pytest.raises(expected_exception) as exc_info:
        M.monitor(*args)
    assert str(exc_info.value) == expected_message