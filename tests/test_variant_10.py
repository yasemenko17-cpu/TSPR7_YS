"""Відкриті тести задачі 10: Зведений звіт: burn-down ризиків.

Запуск: pytest tests/test_variant_10.py
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

FUNC = "burn_down"
CASES = [
    ('T10-S1-1', ([{'sprint': 1,
   'risks': [{'id': 'R-01', 'p': 4, 'i': 4, 'status': 'відкритий'},
             {'id': 'R-02', 'p': 2, 'i': 5, 'status': 'відкритий'},
             {'id': 'R-03', 'p': 3, 'i': 3, 'status': 'відкритий'},
             {'id': 'R-04', 'p': 3, 'i': 4, 'status': 'відкритий'}]},
  {'sprint': 2,
   'risks': [{'id': 'R-01', 'p': 3, 'i': 4, 'status': 'відкритий'},
             {'id': 'R-02', 'p': 2, 'i': 5, 'status': 'стався'},
             {'id': 'R-03', 'p': 3, 'i': 3, 'status': 'відкритий'},
             {'id': 'R-04', 'p': 3, 'i': 4, 'status': 'відкритий'}]},
  {'sprint': 3,
   'risks': [{'id': 'R-01', 'p': 2, 'i': 4, 'status': 'відкритий'},
             {'id': 'R-02', 'p': 2, 'i': 5, 'status': 'стався'},
             {'id': 'R-03', 'p': 3, 'i': 3, 'status': 'закритий'},
             {'id': 'R-04', 'p': 2, 'i': 4, 'status': 'відкритий'}]}],
 (4, 9, 16),
 20), {'rows': [{'sprint': 1, 'open': 4, 'exposure': 47, 'high_plus': 3, 'occurred': 0},
          {'sprint': 2, 'open': 3, 'exposure': 33, 'high_plus': 2, 'occurred': 1},
          {'sprint': 3, 'open': 2, 'exposure': 16, 'high_plus': 0, 'occurred': 1}],
 'trend': 'зменшується',
 'reduction_pct': 66.0,
 'target_sprint': 3}),
    ('T10-S2-1', ([{'sprint': 5,
   'risks': [{'id': 'R-01', 'p': 3, 'i': 4, 'status': 'відкритий'},
             {'id': 'R-02', 'p': 4, 'i': 3, 'status': 'відкритий'}]}],
 (3, 8, 15),
 10), {'rows': [{'sprint': 5, 'open': 2, 'exposure': 24, 'high_plus': 2, 'occurred': 0}],
 'trend': 'недостатньо даних',
 'reduction_pct': 0.0,
 'target_sprint': None}),
    ('T10-S3-1', ([{'sprint': 1,
   'risks': [{'id': 'R-01', 'p': 4, 'i': 4, 'status': 'відкритий'},
             {'id': 'R-03', 'p': 3, 'i': 5, 'status': 'відкритий'}]},
  {'sprint': 2,
   'risks': [{'id': 'R-01', 'p': 4, 'i': 4, 'status': 'закритий'},
             {'id': 'R-03', 'p': 3, 'i': 5, 'status': 'відкритий'}]},
  {'sprint': 3,
   'risks': [{'id': 'R-01', 'p': 4, 'i': 4, 'status': 'закритий'},
             {'id': 'R-03', 'p': 3, 'i': 5, 'status': 'закритий'}]}],
 (5, 9, 15),
 0), {'rows': [{'sprint': 1, 'open': 2, 'exposure': 31, 'high_plus': 2, 'occurred': 0},
          {'sprint': 2, 'open': 1, 'exposure': 15, 'high_plus': 1, 'occurred': 0},
          {'sprint': 3, 'open': 0, 'exposure': 0, 'high_plus': 0, 'occurred': 0}],
 'trend': 'зменшується',
 'reduction_pct': 100.0,
 'target_sprint': 3}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_10(args, expected):
    check(10, FUNC, args, expected)
