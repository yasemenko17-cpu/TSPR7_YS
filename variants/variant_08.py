import operator

def monitor(risks: list, metrics: dict, team: list, max_per_owner: int) -> dict:
    # 1. Перевірка ліміту ризиків на власника
    if not isinstance(max_per_owner, int) or isinstance(max_per_owner, bool) or max_per_owner < 1:
        raise ValueError("Ліміт ризиків на власника має бути цілим не менше 1")
    
    # 2. Перевірка на порожній список ризиків
    if not risks:
        raise ValueError("Реєстр порожній")
        
    op_map = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '==': operator.eq
    }
    
    fired = []
    notify = {}
    load = {}
    
    for r in risks:
        r_id = r["id"]
        owner = r["owner"]
        
        # 3. Перевірка, чи входить власник до команди
        if owner not in team:
            raise ValueError(f"Ризик {r_id}: власник {owner} не входить до команди")
            
        trigger = r["trigger"]
        metric = trigger["metric"]
        op_str = trigger["op"]
        val = trigger["value"]
        
        # 4. Перевірка операції порівняння
        if op_str not in op_map:
            raise ValueError(f"Ризик {r_id}: невідома операція «{op_str}»")
            
        # 5. Перевірка наявності метрики
        if metric not in metrics:
            raise ValueError(f"Ризик {r_id}: немає метрики {metric}")
            
        # Рахуємо загальне навантаження власника
        load[owner] = load.get(owner, 0) + 1
        
        # Перевірка спрацювання тригера
        if op_map[op_str](metrics[metric], val):
            fired.append(r_id)
            if owner not in notify:
                notify[owner] = []
            notify[owner].append(r_id)
            
    # Визначення перевантажених власників (більше за max_per_owner), сортування за абеткою
    overloaded = sorted([o for o, count in load.items() if count > max_per_owner])
    
    # Визначення вільних учасників команди (без ризиків) у порядку списку team
    idle = [member for member in team if member not in load]
    
    return {
        "fired": fired,
        "notify": notify,
        "load": load,
        "overloaded": overloaded,
        "idle": idle
    }