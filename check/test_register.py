"""Перевірка реєстру ризиків: pytest check -q (змінна REGISTER задає інший файл)."""
import os
from pathlib import Path

import pytest
import register_rules as rr

PATH = Path(os.environ.get("REGISTER", rr.ROOT / "register" / "my_register.json"))


@pytest.fixture(scope="module")
def register():
    data = rr.load_register(PATH)
    assert isinstance(data, dict), "реєстр має бути JSON-об'єктом"
    return data


@pytest.mark.parametrize("rule", rr.RULES, ids=lambda r: r.__name__)
def test_rule(register, rule):
    problems = rule(register)
    assert not problems, "; ".join(problems)
