"""Відкриті тести задачі 3: Кількісна оцінка: очікувані грошові й часові втрати.

Запуск: pytest tests/test_variant_03.py
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

FUNC = "exposure"
CASES = [
    ('T03-S1-1', ([{'id': 'R-01', 'pct': 60, 'loss': 90000, 'days': 12},
  {'id': 'R-02', 'pct': 25, 'loss': 120000, 'days': 10}],), {'rows': [{'id': 'R-01', 'emv': 54000.0, 'edays': 7.2}, {'id': 'R-02', 'emv': 30000.0, 'edays': 2.5}],
 'total_emv': 84000.0,
 'total_edays': 9.7,
 'worst_loss': 210000,
 'worst_days': 22}),
    ('T03-S2-1', ([{'id': 'R-04', 'pct': 35, 'loss': 80000, 'days': 0}, {'id': 'R-06', 'pct': 20, 'loss': 150000, 'days': 6}],), {'rows': [{'id': 'R-04', 'emv': 28000.0, 'edays': 0.0}, {'id': 'R-06', 'emv': 30000.0, 'edays': 1.2}],
 'total_emv': 58000.0,
 'total_edays': 1.2,
 'worst_loss': 230000,
 'worst_days': 6}),
    ('T03-S3-1', ([{'id': 'R-07', 'pct': 70, 'loss': 18000, 'days': 3}, {'id': 'R-05', 'pct': 50, 'loss': 25000, 'days': 6}],), {'rows': [{'id': 'R-07', 'emv': 12600.0, 'edays': 2.1}, {'id': 'R-05', 'emv': 12500.0, 'edays': 3.0}],
 'total_emv': 25100.0,
 'total_edays': 5.1,
 'worst_loss': 43000,
 'worst_days': 9}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_03(args, expected):
    check(3, FUNC, args, expected)
