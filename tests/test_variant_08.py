"""Відкриті тести задачі 8: Тригери, власники й сповіщення.

Запуск: pytest tests/test_variant_08.py
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

FUNC = "monitor"
CASES = [
    ('T08-S1-1', ([{'id': 'R-01',
   'owner': 'Софія Гнатюк',
   'trigger': {'metric': 'changed_requirements', 'op': '>', 'value': 3}},
  {'id': 'R-04', 'owner': 'Денис Шевчук', 'trigger': {'metric': 'test_coverage_pct', 'op': '<', 'value': 60}},
  {'id': 'R-05', 'owner': 'Ігор Мельник', 'trigger': {'metric': 'load_peak_pct', 'op': '>', 'value': 80}}],
 {'changed_requirements': 5, 'test_coverage_pct': 55, 'load_peak_pct': 60},
 ['Олена Бойко', 'Ігор Мельник', 'Марта Коваль', 'Денис Шевчук', 'Софія Гнатюк'],
 2), {'fired': ['R-01', 'R-04'],
 'notify': {'Софія Гнатюк': ['R-01'], 'Денис Шевчук': ['R-04']},
 'load': {'Софія Гнатюк': 1, 'Денис Шевчук': 1, 'Ігор Мельник': 1},
 'overloaded': [],
 'idle': ['Олена Бойко', 'Марта Коваль']}),
    ('T08-S2-1', ([{'id': 'R-06',
   'owner': 'Вікторія Сидоренко',
   'trigger': {'metric': 'payment_incidents', 'op': '>=', 'value': 1}},
  {'id': 'R-07',
   'owner': 'Вікторія Сидоренко',
   'trigger': {'metric': 'response_p95_ms', 'op': '>', 'value': 1200}},
  {'id': 'R-03',
   'owner': 'Максим Данилюк',
   'trigger': {'metric': 'device_coverage_pct', 'op': '<', 'value': 80}}],
 {'payment_incidents': 0, 'response_p95_ms': 1500, 'device_coverage_pct': 85},
 ['Андрій Левченко',
  'Катерина Мороз',
  'Тарас Гринюк',
  'Вікторія Сидоренко',
  'Максим Данилюк',
  'Юлія Остапчук'],
 1), {'fired': ['R-07'],
 'notify': {'Вікторія Сидоренко': ['R-07']},
 'load': {'Вікторія Сидоренко': 2, 'Максим Данилюк': 1},
 'overloaded': ['Вікторія Сидоренко'],
 'idle': ['Андрій Левченко', 'Катерина Мороз', 'Тарас Гринюк', 'Юлія Остапчук']}),
    ('T08-S3-1', ([{'id': 'R-06', 'owner': 'Ірина Ткач', 'trigger': {'metric': 'rollback_plan_ready', 'op': '==', 'value': 0}},
  {'id': 'R-03',
   'owner': 'Роман Кравець',
   'trigger': {'metric': 'rehearsal_minutes', 'op': '>', 'value': 240}},
  {'id': 'R-07',
   'owner': 'Оксана Литвин',
   'trigger': {'metric': 'trained_users_pct', 'op': '<', 'value': 70}}],
 {'rollback_plan_ready': 0, 'rehearsal_minutes': 200, 'trained_users_pct': 65},
 ['Павло Заєць', 'Ірина Ткач', 'Роман Кравець', 'Оксана Литвин', 'Богдан Шульга'],
 1), {'fired': ['R-06', 'R-07'],
 'notify': {'Ірина Ткач': ['R-06'], 'Оксана Литвин': ['R-07']},
 'load': {'Ірина Ткач': 1, 'Роман Кравець': 1, 'Оксана Литвин': 1},
 'overloaded': [],
 'idle': ['Павло Заєць', 'Богдан Шульга']}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_08(args, expected):
    check(8, FUNC, args, expected)
