"""Відкриті тести задачі 2: Якісна оцінка: імовірність × вплив і зони матриці.

Запуск: pytest tests/test_variant_02.py
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

FUNC = "qualitative"
CASES = [
    ('T02-S1-1', ([{'id': 'R-01', 'p': 4, 'i': 4}, {'id': 'R-04', 'p': 3, 'i': 4}, {'id': 'R-07', 'p': 1, 'i': 4}], (4, 9, 16)), {'rows': [{'id': 'R-01', 'score': 16, 'zone': 'висока'},
          {'id': 'R-04', 'score': 12, 'zone': 'висока'},
          {'id': 'R-07', 'score': 4, 'zone': 'низька'}],
 'counts': {'низька': 1, 'середня': 0, 'висока': 2, 'критична': 0},
 'matrix': [[[], [], [], [], []],
            [[], [], [], ['R-01'], []],
            [[], [], [], ['R-04'], []],
            [[], [], [], [], []],
            [[], [], [], ['R-07'], []]]}),
    ('T02-S2-1', ([{'id': 'R-02', 'p': 4, 'i': 3}, {'id': 'R-03', 'p': 4, 'i': 3}, {'id': 'R-08', 'p': 2, 'i': 3}], (3, 8, 15)), {'rows': [{'id': 'R-02', 'score': 12, 'zone': 'висока'},
          {'id': 'R-03', 'score': 12, 'zone': 'висока'},
          {'id': 'R-08', 'score': 6, 'zone': 'середня'}],
 'counts': {'низька': 0, 'середня': 1, 'висока': 2, 'критична': 0},
 'matrix': [[[], [], [], [], []],
            [[], [], ['R-02', 'R-03'], [], []],
            [[], [], [], [], []],
            [[], [], ['R-08'], [], []],
            [[], [], [], [], []]]}),
    ('T02-S3-1', ([{'id': 'A', 'p': 5, 'i': 1},
  {'id': 'B', 'p': 4, 'i': 1},
  {'id': 'C', 'p': 3, 'i': 1},
  {'id': 'D', 'p': 2, 'i': 1},
  {'id': 'E', 'p': 1, 'i': 1}],
 (5, 9, 15)), {'rows': [{'id': 'A', 'score': 5, 'zone': 'низька'},
          {'id': 'B', 'score': 4, 'zone': 'низька'},
          {'id': 'C', 'score': 3, 'zone': 'низька'},
          {'id': 'D', 'score': 2, 'zone': 'низька'},
          {'id': 'E', 'score': 1, 'zone': 'низька'}],
 'counts': {'низька': 5, 'середня': 0, 'висока': 0, 'критична': 0},
 'matrix': [[['A'], [], [], [], []],
            [['B'], [], [], [], []],
            [['C'], [], [], [], []],
            [['D'], [], [], [], []],
            [['E'], [], [], [], []]]}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_02(args, expected):
    check(2, FUNC, args, expected)
