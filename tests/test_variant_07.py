"""Відкриті тести задачі 7: Залишковий ризик після мітигації.

Запуск: pytest tests/test_variant_07.py
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

FUNC = "residual"
CASES = [
    ('T07-S1-1', ([{'id': 'R-01', 'p': 4, 'i': 4, 'strategy': 'зниження', 'p_drop': 2},
  {'id': 'R-02', 'p': 2, 'i': 5, 'strategy': 'передача', 'i_drop': 2},
  {'id': 'R-07', 'p': 1, 'i': 4, 'strategy': 'прийняття пасивне'}],
 (4, 9, 16),
 'середня'), {'rows': [{'id': 'R-01',
           'before': 16,
           'after': 8,
           'zone_after': 'середня',
           'secondary_zone': None,
           'ok': True},
          {'id': 'R-02',
           'before': 10,
           'after': 6,
           'zone_after': 'середня',
           'secondary_zone': None,
           'ok': True},
          {'id': 'R-07',
           'before': 4,
           'after': 4,
           'zone_after': 'низька',
           'secondary_zone': None,
           'ok': True}],
 'need_more': [],
 'total_before': 30,
 'total_after': 18,
 'reduction_pct': 40.0}),
    ('T07-S2-1', ([{'id': 'R-02', 'p': 4, 'i': 3, 'strategy': 'зниження', 'p_drop': 2, 'i_drop': 1},
  {'id': 'R-06', 'p': 2, 'i': 5, 'strategy': 'передача', 'i_drop': 1, 'secondary': {'p': 1, 'i': 2}},
  {'id': 'R-08', 'p': 2, 'i': 3, 'strategy': 'ескалація', 'p_drop': 2}],
 (3, 8, 15),
 'середня'), {'rows': [{'id': 'R-02',
           'before': 12,
           'after': 4,
           'zone_after': 'середня',
           'secondary_zone': None,
           'ok': True},
          {'id': 'R-06',
           'before': 10,
           'after': 8,
           'zone_after': 'середня',
           'secondary_zone': 'низька',
           'ok': True},
          {'id': 'R-08',
           'before': 6,
           'after': 6,
           'zone_after': 'середня',
           'secondary_zone': None,
           'ok': True}],
 'need_more': [],
 'total_before': 28,
 'total_after': 18,
 'reduction_pct': 35.7}),
    ('T07-S3-1', ([{'id': 'R-01', 'p': 4, 'i': 4, 'strategy': 'уникнення'},
  {'id': 'R-03',
   'p': 3,
   'i': 5,
   'strategy': 'зниження',
   'p_drop': 2,
   'i_drop': 1,
   'secondary': {'p': 2, 'i': 4}},
  {'id': 'R-02', 'p': 2, 'i': 5, 'strategy': 'зниження', 'p_drop': 0, 'i_drop': 0}],
 (5, 9, 15),
 'середня'), {'rows': [{'id': 'R-01', 'before': 16, 'after': 0, 'zone_after': 'знято', 'secondary_zone': None, 'ok': True},
          {'id': 'R-03',
           'before': 15,
           'after': 4,
           'zone_after': 'низька',
           'secondary_zone': 'середня',
           'ok': True},
          {'id': 'R-02',
           'before': 10,
           'after': 10,
           'zone_after': 'висока',
           'secondary_zone': None,
           'ok': False}],
 'need_more': ['R-02'],
 'total_before': 41,
 'total_after': 14,
 'reduction_pct': 65.9}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_07(args, expected):
    check(7, FUNC, args, expected)
