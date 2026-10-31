"""Персистентность (аналог хука useLocalStorage).

Состояние живёт в st.session_state["char"], а после каждого изменения
сохраняется в JSON-файл на диске (data/character.json).
Путь можно переопределить переменной окружения STRATEGIST_DATA.
"""
import json
import os
from pathlib import Path

import streamlit as st

from demo import demo_character
from models import Character

DATA_FILE = Path(os.environ.get("STRATEGIST_DATA",
                                Path(__file__).parent / "data" / "character.json"))


def _read() -> Character | None:
    try:
        return Character.from_dict(json.loads(DATA_FILE.read_text("utf-8")))
    except (OSError, ValueError):
        return None


def save(char: Character) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_FILE.with_suffix(".tmp")  # атомарная запись
    tmp.write_text(json.dumps(char.to_dict(), ensure_ascii=False, indent=2), "utf-8")
    tmp.replace(DATA_FILE)


def get_char() -> Character:
    if "char" not in st.session_state:
        st.session_state.char = _read() or demo_character()
        save(st.session_state.char)
    return st.session_state.char


def commit() -> None:
    """Сохранить текущее состояние на диск."""
    save(st.session_state.char)


def clear_keys(prefix: str) -> None:
    """Удалить состояния виджетов с префиксом (нужно после удаления элементов списка)."""
    for k in [k for k in st.session_state if str(k).startswith(prefix)]:
        del st.session_state[k]


def replace_char(new: Character) -> None:
    """Полная замена персонажа (импорт / сброс). Сбрасывает состояние всех виджетов."""
    for k in [k for k in st.session_state if k != "char"]:
        del st.session_state[k]
    st.session_state.char = new
    commit()
