"""Відкриті тести задачі 6: Резерв на ризики.

Запуск: pytest tests/test_variant_06.py
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

FUNC = "contingency"
CASES = [
    ('T06-S1-1', ([{'id': 'R-01', 'strategy': 'зниження', 'pct': 60, 'loss': 90000, 'days': 12, 'response_cost': 12000},
  {'id': 'R-03', 'strategy': 'зниження', 'pct': 40, 'loss': 30000, 'days': 10, 'response_cost': 8000},
  {'id': 'R-04', 'strategy': 'прийняття активне', 'pct': 35, 'loss': 60000, 'days': 5},
  {'id': 'R-02', 'strategy': 'передача', 'pct': 25, 'loss': 120000, 'days': 10, 'response_cost': 15000},
  {'id': 'R-07', 'strategy': 'прийняття пасивне', 'pct': 10, 'loss': 40000, 'days': 8}],
 {'budget': 600000, 'days': 80},
 15), {'covered': ['R-01', 'R-03', 'R-04'],
 'money': 87000,
 'days': 13,
 'response_cost': 35000,
 'total_budget': 722000,
 'pct_of_budget': 14.5,
 'within_cap': True}),
    ('T06-S2-1', ([{'id': 'R-02', 'strategy': 'зниження', 'pct': 65, 'loss': 36000, 'days': 4, 'response_cost': 20000},
  {'id': 'R-03', 'strategy': 'зниження', 'pct': 55, 'loss': 45000, 'days': 3, 'response_cost': 16000},
  {'id': 'R-04', 'strategy': 'передача', 'pct': 35, 'loss': 80000, 'days': 0, 'response_cost': 15000},
  {'id': 'R-08', 'strategy': 'ескалація', 'pct': 25, 'loss': 40000, 'days': 8}],
 {'budget': 900000, 'days': 100},
 12), {'covered': ['R-02', 'R-03'],
 'money': 48200,
 'days': 5,
 'response_cost': 51000,
 'total_budget': 999200,
 'pct_of_budget': 5.4,
 'within_cap': True}),
    ('T06-S3-1', ([{'id': 'R-01', 'strategy': 'уникнення', 'pct': 60, 'loss': 60000, 'days': 5, 'response_cost': 10000},
  {'id': 'R-02', 'strategy': 'прийняття активне', 'pct': 20, 'loss': 100000, 'days': 6},
  {'id': 'R-05', 'strategy': 'зниження', 'pct': 50, 'loss': 25000, 'days': 6, 'response_cost': 9000},
  {'id': 'R-07', 'strategy': 'зниження', 'pct': 70, 'loss': 18000, 'days': 3, 'response_cost': 5000}],
 {'budget': 450000, 'days': 60},
 20), {'covered': ['R-02', 'R-05', 'R-07'],
 'money': 45100,
 'days': 7,
 'response_cost': 24000,
 'total_budget': 519100,
 'pct_of_budget': 10.0,
 'within_cap': True}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_06(args, expected):
    check(6, FUNC, args, expected)
