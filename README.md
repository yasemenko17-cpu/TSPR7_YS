# Стартовий проєкт TSPP-P07

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Реалізуйте задачу у файлі `variants/variant_NN.py` за карткою.
3. Запускайте відкриті тести своєї задачі: `pytest tests/test_variant_NN.py` (NN з двома цифрами). Права адміністратора не потрібні.
4. Дані проєктних контекстів лежать у `data/` (файл вашого набору: `context_N_*.json`). Вони потрібні для прикладів і самостійних вправ.
5. Реєстр ризиків власного проєкту складайте у `register/my_register.json`; формат показано в `register/format_example.json`. Перевірка: `pytest check -q` (змінна `REGISTER` задає інший файл). Тести в `check/` не входять до `pytest tests`.
6. Змінюйте лише свій файл у `variants/`, файл `tests/test_my.py`, `register/my_register.json` і `ANSWERS.md`.
