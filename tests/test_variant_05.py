"""Відкриті тести задачі 5: Вибір стратегії реагування за правилами.

Запуск: pytest tests/test_variant_05.py
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

FUNC = "choose_strategies"
CASES = [
    ('T05-S1-1', ([{'id': 'R-1', 'kind': 'threat', 'zone': 'критична', 'emv': 12000, 'avoidable': True, 'mitigate_cost': 3000},
  {'id': 'R-2',
   'kind': 'threat',
   'zone': 'висока',
   'emv': 30000,
   'transfer_cost': 9000,
   'mitigate_cost': 4000},
  {'id': 'R-3', 'kind': 'threat', 'zone': 'низька', 'emv': 800}],), [{'id': 'R-1', 'strategy': 'уникнення', 'rule': 'T2'},
 {'id': 'R-2', 'strategy': 'передача', 'rule': 'T3'},
 {'id': 'R-3', 'strategy': 'прийняття пасивне', 'rule': 'T5'}]),
    ('T05-S2-1', ([{'id': 'R-6', 'kind': 'threat', 'zone': 'висока', 'emv': 30000, 'avoidable': True, 'mitigate_cost': 25000},
  {'id': 'R-7', 'kind': 'threat', 'zone': 'критична', 'emv': 24500, 'avoidable': True}],), [{'id': 'R-6', 'strategy': 'зниження', 'rule': 'T4'}, {'id': 'R-7', 'strategy': 'уникнення', 'rule': 'T2'}]),
    ('T05-S3-1', ([{'id': 'R-4',
   'kind': 'threat',
   'zone': 'висока',
   'emv': 18000,
   'transfer_cost': 12000,
   'mitigate_cost': 1000},
  {'id': 'R-9', 'kind': 'threat', 'zone': 'критична', 'emv': 50000, 'avoidable': True, 'scope': 'org'}],), [{'id': 'R-4', 'strategy': 'передача', 'rule': 'T3'}, {'id': 'R-9', 'strategy': 'ескалація', 'rule': 'T1'}]),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_05(args, expected):
    check(5, FUNC, args, expected)
