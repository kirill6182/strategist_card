# ♟️ Карточка персонажа-стратега (Python / Streamlit)

RPG-трекер личного развития: статы, баффы/дебаффы, сильные и слабые стороны,
миссия и дневник. Смотри на себя как стратег — от третьего лица.

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Откроется http://localhost:8501. Нужен Python 3.10+ и Streamlit 1.37+.

## Где хранятся данные
В `data/character.json` рядом с приложением (аналог localStorage).
Файл создаётся при первом запуске с демо-данными и обновляется после каждого
действия. Другой путь: переменная окружения `STRATEGIST_DATA`.
Экспорт/импорт JSON совместим по формату с TypeScript-интерфейсом из ТЗ (camelCase).

## Управление
- Статы: кнопки «−» / «+» (в Streamlit нет правого клика и долгого нажатия).
- «＋ Опыт»: +5–10% XP; при 100% уровень +1, XP = 0.
- Настройки (⚙️): сброс к демо-данным с подтверждением.

## Архитектура
- `app.py` — точка входа, собирает панели сверху вниз.
- `models.py` — типы (dataclass) + валидация и JSON-сериализация (аналог types.ts).
- `storage.py` — загрузка/сохранение, `session_state` + файл (аналог useLocalStorage).
- `demo.py` — демо-персонаж; `styles.py` — тёмная неоновая тема (CSS).
- `components/` — Header, StatsPanel, EffectsPanel, MissionPanel, DiaryPanel, Settings.
- Изменения идут через callback-функции (`on_click`/`on_change`), которые меняют модель и вызывают `commit()`.
