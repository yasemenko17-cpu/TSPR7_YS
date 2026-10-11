"""Відкриті тести задачі 9: Оновлення реєстру за подіями спринту.

Запуск: pytest tests/test_variant_09.py
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

FUNC = "apply_events"
CASES = [
    ('T09-S1-1', ([{'id': 'R-01', 'p': 4, 'i': 4, 'status': 'відкритий'},
  {'id': 'R-02', 'p': 2, 'i': 5, 'status': 'відкритий'},
  {'id': 'R-03', 'p': 3, 'i': 3, 'status': 'відкритий'}],
 [{'sprint': 1, 'type': 'reassess', 'id': 'R-01', 'p': 3},
  {'sprint': 1, 'type': 'occurred', 'id': 'R-02'},
  {'sprint': 2, 'type': 'new', 'id': 'R-09', 'p': 2, 'i': 3},
  {'sprint': 2, 'type': 'closed', 'id': 'R-03'}]), {'register': [{'id': 'R-01', 'p': 3, 'i': 4, 'status': 'відкритий', 'score': 12},
              {'id': 'R-02', 'p': 2, 'i': 5, 'status': 'стався', 'score': 10},
              {'id': 'R-03', 'p': 3, 'i': 3, 'status': 'закритий', 'score': 9},
              {'id': 'R-09', 'p': 2, 'i': 3, 'status': 'відкритий', 'score': 6}],
 'log': [{'sprint': 1, 'id': 'R-01', 'action': 'переоцінено'},
         {'sprint': 1, 'id': 'R-02', 'action': 'стався'},
         {'sprint': 2, 'id': 'R-09', 'action': 'додано'},
         {'sprint': 2, 'id': 'R-03', 'action': 'закрито'}],
 'counts': {'відкритий': 2, 'стався': 1, 'закритий': 1}}),
    ('T09-S2-1', ([{'id': 'R-01', 'p': 3, 'i': 4, 'status': 'відкритий'},
  {'id': 'R-02', 'p': 4, 'i': 3, 'status': 'відкритий'},
  {'id': 'R-03', 'p': 4, 'i': 3, 'status': 'відкритий'}],
 [{'sprint': 1, 'type': 'occurred', 'id': 'R-02'},
  {'sprint': 2, 'type': 'new', 'id': 'R-09', 'p': 3, 'i': 3},
  {'sprint': 2, 'type': 'reassess', 'id': 'R-03', 'p': 3}]), {'register': [{'id': 'R-01', 'p': 3, 'i': 4, 'status': 'відкритий', 'score': 12},
              {'id': 'R-02', 'p': 4, 'i': 3, 'status': 'стався', 'score': 12},
              {'id': 'R-03', 'p': 3, 'i': 3, 'status': 'відкритий', 'score': 9},
              {'id': 'R-09', 'p': 3, 'i': 3, 'status': 'відкритий', 'score': 9}],
 'log': [{'sprint': 1, 'id': 'R-02', 'action': 'стався'},
         {'sprint': 2, 'id': 'R-09', 'action': 'додано'},
         {'sprint': 2, 'id': 'R-03', 'action': 'переоцінено'}],
 'counts': {'відкритий': 3, 'стався': 1, 'закритий': 0}}),
    ('T09-S3-1', ([{'id': 'R-02', 'p': 2, 'i': 5, 'status': 'відкритий'},
  {'id': 'R-06', 'p': 2, 'i': 5, 'status': 'відкритий'},
  {'id': 'R-03', 'p': 3, 'i': 5, 'status': 'відкритий'}],
 [{'sprint': 1, 'type': 'closed', 'id': 'R-06'},
  {'sprint': 2, 'type': 'reassess', 'id': 'R-03', 'p': 2, 'i': 4},
  {'sprint': 2, 'type': 'new', 'id': 'R-10', 'p': 2, 'i': 3}]), {'register': [{'id': 'R-02', 'p': 2, 'i': 5, 'status': 'відкритий', 'score': 10},
              {'id': 'R-06', 'p': 2, 'i': 5, 'status': 'закритий', 'score': 10},
              {'id': 'R-03', 'p': 2, 'i': 4, 'status': 'відкритий', 'score': 8},
              {'id': 'R-10', 'p': 2, 'i': 3, 'status': 'відкритий', 'score': 6}],
 'log': [{'sprint': 1, 'id': 'R-06', 'action': 'закрито'},
         {'sprint': 2, 'id': 'R-03', 'action': 'переоцінено'},
         {'sprint': 2, 'id': 'R-10', 'action': 'додано'}],
 'counts': {'відкритий': 3, 'стався': 0, 'закритий': 1}}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_09(args, expected):
    check(9, FUNC, args, expected)
