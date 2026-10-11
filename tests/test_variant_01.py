"""Відкриті тести задачі 1: Формулювання ризику за шаблоном «причина → подія → наслідок».

Запуск: pytest tests/test_variant_01.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


def check(number, func, args, expected):
    call = getattr(load(number), func)
    before = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            call(*args)
        assert str(info.value) == str(expected)
    else:
        result = call(*args)
        assert norm(result) == norm(expected)
        assert type(result) is type(expected)
    assert args == before, "функція не повинна змінювати вхідні дані"

FUNC = "parse_statement"
CASES = [
    ('T01-S1-1', ('Через нечіткі вимоги до кошика → замовник змінить сценарій оформлення → доведеться переробляти модуль',), {'cause': 'Через нечіткі вимоги до кошика',
 'event': 'замовник змінить сценарій оформлення',
 'consequence': 'доведеться переробляти модуль',
 'area': 'обсяг'}),
    ('T01-S2-1', ('Через довгу перевірку магазином застосунків → випуск iOS-версії затримається → не вдасться почати пілот у '
 'заплановану дату',), {'cause': 'Через довгу перевірку магазином застосунків',
 'event': 'випуск iOS-версії затримається',
 'consequence': 'не вдасться почати пілот у заплановану дату',
 'area': 'інше'}),
    ('T01-S3-1', ('Через затримку постачання обладнання → нові сервери прибудуть пізніше → затримка міграції й додаткові '
 'витрати на оренду',), {'cause': 'Через затримку постачання обладнання',
 'event': 'нові сервери прибудуть пізніше',
 'consequence': 'затримка міграції й додаткові витрати на оренду',
 'area': 'строки'}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_01(args, expected):
    check(1, FUNC, args, expected)
