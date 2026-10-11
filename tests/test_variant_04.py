"""Відкриті тести задачі 4: Ранжування ризиків і топ-N.

Запуск: pytest tests/test_variant_04.py
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

FUNC = "top_risks"
CASES = [
    ('T04-S1-1', ([{'id': 'R-01', 'p': 4, 'i': 4, 'loss': 90000},
  {'id': 'R-02', 'p': 2, 'i': 5, 'loss': 120000},
  {'id': 'R-04', 'p': 3, 'i': 4, 'loss': 60000},
  {'id': 'R-03', 'p': 3, 'i': 3, 'loss': 30000}],
 2), {'top': ['R-01', 'R-04'],
 'ranks': [{'rank': 1, 'id': 'R-01', 'score': 16},
           {'rank': 2, 'id': 'R-04', 'score': 12},
           {'rank': 3, 'id': 'R-02', 'score': 10},
           {'rank': 4, 'id': 'R-03', 'score': 9}],
 'share': 59.6}),
    ('T04-S2-1', ([{'id': 'R-01', 'p': 4, 'i': 3, 'loss': 50000},
  {'id': 'R-07', 'p': 3, 'i': 4, 'loss': 70000},
  {'id': 'R-03', 'p': 4, 'i': 3, 'loss': 45000}],
 3), {'top': ['R-07', 'R-01', 'R-03'],
 'ranks': [{'rank': 1, 'id': 'R-07', 'score': 12},
           {'rank': 2, 'id': 'R-01', 'score': 12},
           {'rank': 3, 'id': 'R-03', 'score': 12}],
 'share': 100.0}),
    ('T04-S3-1', ([{'id': 'R-01', 'p': 4, 'i': 4, 'loss': 60000},
  {'id': 'R-03', 'p': 3, 'i': 5, 'loss': 90000},
  {'id': 'R-04', 'p': 3, 'i': 4, 'loss': 40000},
  {'id': 'R-07', 'p': 4, 'i': 2, 'loss': 18000}],
 1), {'top': ['R-01'],
 'ranks': [{'rank': 1, 'id': 'R-01', 'score': 16},
           {'rank': 2, 'id': 'R-03', 'score': 15},
           {'rank': 3, 'id': 'R-04', 'score': 12},
           {'rank': 4, 'id': 'R-07', 'score': 8}],
 'share': 31.4}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_04(args, expected):
    check(4, FUNC, args, expected)
