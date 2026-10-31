import html
import random

import streamlit as st

from components import settings
from storage import commit, get_char


def _on_name_change() -> None:
    char = get_char()
    new = st.session_state.name_input.strip()
    if not new:  # валидация: имя не пустое
        st.session_state.name_input = char.name
        st.toast("Имя не может быть пустым", icon="⚠️")
        return
    char.name = new
    commit()


def _add_xp() -> None:
    char = get_char()
    char.xp += random.randint(5, 10)
    if char.xp >= 100:
        char.level += 1
        char.xp = 0
        st.toast(f"Новый уровень: {char.level}!", icon="🎉")
    commit()


def render() -> None:
    char = get_char()
    c1, c2, c3 = st.columns([4, 2, 1])
    with c1:
        st.text_input("Имя персонажа", value=char.name, key="name_input",
                      on_change=_on_name_change, max_chars=40)
    with c2:
        st.markdown(
            f'<div style="padding-top:1.7rem"><span class="badge">♟️ {html.escape(char.class_name)}</span> '
            f'&nbsp;<span class="lvl mono">LVL {char.level}</span></div>',
            unsafe_allow_html=True)
    with c3:
        st.markdown('<div style="padding-top:1.7rem"></div>', unsafe_allow_html=True)
        if st.button("⚙️ Настройки", key="open_settings"):
            settings.settings_dialog()

    st.markdown(
        f'<div class="xp-track"><div class="xp-fill" style="width:{char.xp}%"></div></div>'
        f'<div class="xp-label mono">XP {char.xp}/100</div>', unsafe_allow_html=True)
    st.button("＋ Опыт", on_click=_add_xp, key="add_xp")
