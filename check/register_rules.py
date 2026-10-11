"""Правила перевірки реєстру ризиків (форма й узгодженість, а не зміст).

Реєстр лежить у файлі register/my_register.json; формат показано в register/format_example.json.
Кожне правило повертає список зауважень; порожній список означає, що правило виконано.
Запуск: pytest check -q (змінна REGISTER задає інший файл).
"""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZONES = ("низька", "середня", "висока", "критична")
CATEGORIES = ("технічний", "організаційний", "зовнішній", "управлінський")
STRATEGIES = ("ескалація", "уникнення", "передача", "зниження", "прийняття пасивне", "прийняття активне")
COVERED = ("зниження", "прийняття активне")
SPENT = ("уникнення", "передача", "зниження")
OPS = ("<", "<=", ">", ">=", "==")
BANDS = {1: (1, 10), 2: (11, 30), 3: (31, 50), 4: (51, 70), 5: (71, 100)}
TOP = ("project", "scale", "risks", "reserve", "review")
RISK_KEYS = ("id", "text", "category", "p", "i", "score", "zone", "pct", "loss", "days", "emv", "strategy",
             "action", "response_cost", "p_after", "i_after", "residual_score", "owner", "trigger")
MAX_PER_OWNER = 4


def load_register(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_num(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def words(text):
    return len(str(text).split())


def zone_of(score, bounds):
    return ZONES[sum(score > b for b in bounds)]


def bounds_ok(bounds):
    return (isinstance(bounds, list) and len(bounds) == 3 and all(is_int(b) for b in bounds)
            and 1 <= bounds[0] < bounds[1] < bounds[2] <= 24)


def risks_of(reg):
    items = reg.get("risks")
    return [r for r in items if isinstance(r, dict)] if isinstance(items, list) else []


def statement_problems(text):
    """Три частини через «→», кожна не менше двох слів, усі різні."""
    if not isinstance(text, str) or not text.strip():
        return ["порожнє формулювання"]
    parts = [p.strip() for p in text.split("→")]
    if len(parts) != 3:
        return [f"потрібно три частини, розділені «→»: знайдено {len(parts)}"]
    names = ("причина", "подія", "наслідок")
    out = [f"порожня частина: {n}" for n, p in zip(names, parts) if not p]
    if out:
        return out
    out = [f"частина «{n}» має містити щонайменше два слова" for n, p in zip(names, parts) if len(p.split()) < 2]
    if not out and len({p.casefold() for p in parts}) < 3:
        out.append("причина, подія й наслідок мають відрізнятися")
    return out


def rule_structure(reg, _=None):
    problems = [f"немає поля {k}" for k in TOP if k not in reg]
    for r in risks_of(reg):
        miss = [k for k in RISK_KEYS if k not in r]
        if miss:
            problems.append(f"ризик {r.get('id', '?')}: немає полів {', '.join(miss)}")
    if not isinstance(reg.get("risks", []), list):
        problems.append("risks має бути списком")
    return problems


def rule_project(reg, _=None):
    p = reg.get("project")
    if not isinstance(p, dict):
        return ["project має бути об'єктом"]
    problems = []
    if words(p.get("name", "")) < 2:
        problems.append("project.name: потрібна назва щонайменше з двох слів")
    if words(p.get("goal", "")) < 4:
        problems.append("project.goal: опишіть мету щонайменше чотирма словами")
    if not is_int(p.get("budget")) or p["budget"] <= 0:
        problems.append("project.budget: потрібне додатне ціле число (грн)")
    if not is_int(p.get("duration_weeks")) or not 1 <= p["duration_weeks"] <= 104:
        problems.append("project.duration_weeks: ціле число тижнів від 1 до 104")
    team = p.get("team")
    if not isinstance(team, list) or len(team) < 2 or len(set(team)) != len(team) or not all(isinstance(t, str) and t.strip() for t in team):
        problems.append("project.team: щонайменше двоє різних учасників (рядки)")
    return problems


def rule_risks(reg, _=None):
    risks = risks_of(reg)
    problems = []
    if len(risks) < 8:
        problems.append(f"у реєстрі потрібно щонайменше 8 ризиків, зараз {len(risks)}")
    ids = [r.get("id") for r in risks]
    if len(set(ids)) != len(ids):
        problems.append("ідентифікатори ризиків мають бути унікальними")
    for rid in ids:
        if not isinstance(rid, str) or not re.fullmatch(r"R-\d{2}", rid):
            problems.append(f"ідентифікатор {rid!r}: потрібен вигляд R-01")
    cats = [r.get("category") for r in risks]
    if any(c not in CATEGORIES for c in cats):
        problems.append("категорія має бути однією з: " + ", ".join(CATEGORIES))
    elif len(set(cats)) < 3:
        problems.append("потрібні щонайменше три різні категорії ризиків")
    return problems


def rule_statements(reg, _=None):
    problems = []
    for r in risks_of(reg):
        for p in statement_problems(r.get("text")):
            problems.append(f"ризик {r.get('id', '?')}: {p}")
    return problems


def rule_assessment(reg, _=None):
    scale = reg.get("scale")
    if not isinstance(scale, dict) or not bounds_ok(scale.get("bounds")):
        return ["scale.bounds: три зростаючі цілі межі зон від 1 до 24"]
    problems = []
    if scale.get("tolerance") not in ZONES:
        problems.append("scale.tolerance: одна з зон " + ", ".join(ZONES))
    scores = set()
    for r in risks_of(reg):
        rid = r.get("id", "?")
        p, i = r.get("p"), r.get("i")
        if not (is_int(p) and 1 <= p <= 5 and is_int(i) and 1 <= i <= 5):
            problems.append(f"ризик {rid}: p і i мають бути цілими від 1 до 5")
            continue
        scores.add(p * i)
        if r.get("score") != p * i:
            problems.append(f"ризик {rid}: score {r.get('score')} не дорівнює p × i = {p * i}")
        if r.get("zone") != zone_of(p * i, scale["bounds"]):
            problems.append(f"ризик {rid}: зона має бути «{zone_of(p * i, scale['bounds'])}»")
    if len(risks_of(reg)) >= 8 and len(scores) < 3:
        problems.append("оцінки ризиків мають відрізнятися: потрібні щонайменше три різні значення score")
    return problems


def rule_quant(reg, _=None):
    problems = []
    for r in risks_of(reg):
        rid = r.get("id", "?")
        pct, loss, days = r.get("pct"), r.get("loss"), r.get("days")
        if not (is_int(pct) and 1 <= pct <= 100):
            problems.append(f"ризик {rid}: pct має бути цілим від 1 до 100")
            continue
        if not (is_int(loss) and loss >= 0 and is_int(days) and days >= 0):
            problems.append(f"ризик {rid}: loss і days мають бути цілими невід'ємними")
            continue
        if is_int(r.get("p")) and r["p"] in BANDS and not BANDS[r["p"]][0] <= pct <= BANDS[r["p"]][1]:
            lo, hi = BANDS[r["p"]]
            problems.append(f"ризик {rid}: імовірності p = {r['p']} відповідає pct від {lo} до {hi}, а не {pct}")
        if not is_num(r.get("emv")) or abs(r["emv"] - pct * loss / 100) > 0.01:
            problems.append(f"ризик {rid}: emv має дорівнювати pct × loss / 100 = {round(pct * loss / 100, 2)}")
    return problems


def rule_response(reg, _=None):
    problems = []
    for r in risks_of(reg):
        rid = r.get("id", "?")
        s = r.get("strategy")
        if s not in STRATEGIES:
            problems.append(f"ризик {rid}: стратегія має бути однією з: " + ", ".join(STRATEGIES))
            continue
        if words(r.get("action", "")) < 4:
            problems.append(f"ризик {rid}: опишіть дію щонайменше чотирма словами")
        if r.get("zone") in ("висока", "критична") and s == "прийняття пасивне":
            problems.append(f"ризик {rid}: для зони «{r['zone']}» пасивне прийняття не допускається")
        cost = r.get("response_cost")
        if not is_int(cost) or cost < 0:
            problems.append(f"ризик {rid}: response_cost має бути цілим невід'ємним")
        elif s in SPENT and cost == 0:
            problems.append(f"ризик {rid}: стратегія «{s}» потребує ненульової вартості заходу")
    return problems


def rule_owners(reg, _=None):
    team = reg.get("project", {}).get("team", []) if isinstance(reg.get("project"), dict) else []
    problems, load = [], {}
    for r in risks_of(reg):
        rid = r.get("id", "?")
        owner = r.get("owner")
        if owner not in team:
            problems.append(f"ризик {rid}: власник {owner!r} не входить до project.team")
        else:
            load[owner] = load.get(owner, 0) + 1
        t = r.get("trigger")
        if not isinstance(t, dict):
            problems.append(f"ризик {rid}: trigger має бути об'єктом metric, op, value")
            continue
        if not isinstance(t.get("metric"), str) or not t["metric"].strip():
            problems.append(f"ризик {rid}: trigger.metric має бути непорожнім рядком")
        if t.get("op") not in OPS:
            problems.append(f"ризик {rid}: trigger.op має бути однією з: " + ", ".join(OPS))
        if not is_num(t.get("value")):
            problems.append(f"ризик {rid}: trigger.value має бути числом")
    for owner, n in load.items():
        if n > MAX_PER_OWNER:
            problems.append(f"власник {owner} має {n} ризиків, а допускається не більше {MAX_PER_OWNER}")
    return problems


def rule_residual(reg, _=None):
    problems = []
    for r in risks_of(reg):
        rid = r.get("id", "?")
        p, i, pa, ia = r.get("p"), r.get("i"), r.get("p_after"), r.get("i_after")
        s = r.get("strategy")
        if not (is_int(p) and is_int(i) and is_int(pa) and is_int(ia)):
            problems.append(f"ризик {rid}: p_after і i_after мають бути цілими")
            continue
        if not (0 <= pa <= p and 1 <= ia <= i):
            problems.append(f"ризик {rid}: після реагування p_after (0..{p}) та i_after (1..{i}) не можуть зростати")
            continue
        if r.get("residual_score") != pa * ia:
            problems.append(f"ризик {rid}: residual_score має дорівнювати p_after × i_after = {pa * ia}")
        if pa == 0 and s != "уникнення":
            problems.append(f"ризик {rid}: p_after = 0 можливий лише для стратегії «уникнення»")
        if s == "уникнення" and pa != 0:
            problems.append(f"ризик {rid}: уникнення має дати p_after = 0")
        if s in ("зниження", "передача") and pa * ia >= p * i:
            problems.append(f"ризик {rid}: «{s}» має зменшити оцінку: residual_score менший за score")
        if s in ("ескалація", "прийняття пасивне", "прийняття активне") and (pa, ia) != (p, i):
            problems.append(f"ризик {rid}: «{s}» не змінює оцінку: p_after, i_after мають збігатися з p, i")
    return problems


def rule_reserve(reg, _=None):
    res, proj, scale = reg.get("reserve"), reg.get("project"), reg.get("scale")
    if not isinstance(res, dict) or not isinstance(proj, dict) or not is_int(proj.get("budget")) or proj["budget"] <= 0:
        return ["reserve має бути об'єктом із полями money, days, pct_of_budget (потрібен коректний project.budget)"]
    raw_money = raw_days = 0
    for r in risks_of(reg):
        if r.get("strategy") in COVERED and is_int(r.get("pct")) and is_int(r.get("loss")) and is_int(r.get("days")):
            raw_money += r["pct"] * r["loss"]
            raw_days += r["pct"] * r["days"]
    money = -(-raw_money // 10000) * 100
    days = -(-raw_days // 100)
    problems = []
    if res.get("money") != money:
        problems.append(f"reserve.money має дорівнювати {money} (сума pct × loss / 100 для зниження й активного прийняття, угору до сотні)")
    if res.get("days") != days:
        problems.append(f"reserve.days має дорівнювати {days}")
    share = round(100 * money / proj["budget"], 1)
    if not is_num(res.get("pct_of_budget")) or abs(res["pct_of_budget"] - share) > 0.05:
        problems.append(f"reserve.pct_of_budget має дорівнювати {share}")
    cap = scale.get("reserve_cap_pct") if isinstance(scale, dict) else None
    if not is_int(cap) or not 1 <= cap <= 100:
        problems.append("scale.reserve_cap_pct: ціле від 1 до 100")
    elif money * 100 > proj["budget"] * cap:
        problems.append(f"резерв {money} грн перевищує {cap} відсотків бюджету")
    return problems


def rule_review(reg, _=None):
    rev = reg.get("review")
    if not isinstance(rev, list) or len(rev) < 2:
        return ["review: потрібно щонайменше два записи {sprint, note}"]
    problems, last = [], 0
    for e in rev:
        if not isinstance(e, dict) or not is_int(e.get("sprint")) or e["sprint"] < 1:
            problems.append("кожен запис review має ціле sprint від 1")
            continue
        if e["sprint"] <= last:
            problems.append("номери спринтів у review мають зростати")
        last = e["sprint"]
        if words(e.get("note", "")) < 4:
            problems.append(f"спринт {e['sprint']}: нотатка потребує щонайменше чотирьох слів")
    return problems


RULES = [rule_structure, rule_project, rule_risks, rule_statements, rule_assessment, rule_quant,
         rule_response, rule_owners, rule_residual, rule_reserve, rule_review]
