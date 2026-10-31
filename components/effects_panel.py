"""Баффы/дебаффы (Effect) и сильные/слабые стороны (редактируемые строки)."""
import html

import streamlit as st

from models import Effect, new_id
from storage import clear_keys, commit, get_char

EFFECTS = {
    "buffs": ("✨ Баффы", "✨", "Добавь свой первый бафф"),
    "debuffs": ("⚠️ Дебаффы", "⚠️", "Дебаффов нет — отметь первое, что тебя тормозит"),
}
TRAITS = {
    "strengths": ("✅ Сильные стороны", "✅", "Добавь свою первую сильную сторону"),
    "weaknesses": ("❌ Слабые стороны", "❌", "Честно назови первую слабую сторону"),
}


def _empty(icon: str, text: str) -> None:
    st.markdown(f'<div class="empty"><span class="ico">{icon}</span>{html.escape(text)}</div>',
                unsafe_allow_html=True)


# ---------- баффы / дебаффы ----------
def _add_effect(kind: str) -> None:
    ss = st.session_state
    name = ss[f"{kind}_new_name"].strip()
    if not name:
        st.toast("Название не может быть пустым", icon="⚠️")
        return
    getattr(get_char(), kind).append(Effect(new_id(), name, ss[f"{kind}_new_desc"].strip()))
    commit()


def _del_effect(kind: str, effect_id: str) -> None:
    lst = getattr(get_char(), kind)
    lst[:] = [e for e in lst if e.id != effect_id]
    commit()


def _render_effects(kind: str) -> None:
    title, icon, empty = EFFECTS[kind]
    st.markdown(f'<div class="panel-title">{title}</div>', unsafe_allow_html=True)
    items = getattr(get_char(), kind)
    if not items:
        _empty(icon, empty)
    for e in items:
        a, b = st.columns([6, 1])
        desc = f"<span>{html.escape(e.description)}</span>" if e.description else ""
        a.markdown(f'<div class="effect {kind}"><b>{html.escape(e.name)}</b>{desc}</div>',
                   unsafe_allow_html=True)
        b.button("🗑", key=f"del_{kind}_{e.id}", on_click=_del_effect, args=(kind, e.id))
    with st.form(f"{kind}_form", clear_on_submit=True, border=False):
        st.text_input("Название", key=f"{kind}_new_name", placeholder="+ добавить…")
        st.text_input("Описание (необязательно)", key=f"{kind}_new_desc")
        st.form_submit_button("＋ Добавить", on_click=_add_effect, args=(kind,))


# ---------- сильные / слабые стороны ----------
def _add_trait(kind: str) -> None:
    val = st.session_state[f"{kind}_new"].strip()
    if not val:
        st.toast("Пустую строку добавить нельзя", icon="⚠️")
        return
    getattr(get_char(), kind).append(val)
    commit()


def _edit_trait(kind: str, i: int) -> None:
    lst = getattr(get_char(), kind)
    val = st.session_state[f"{kind}_item_{i}"].strip()
    if val:
        lst[i] = val
    else:  # пустая строка = удаление
        del lst[i]
        clear_keys(f"{kind}_item_")
    commit()


def _del_trait(kind: str, i: int) -> None:
    del getattr(get_char(), kind)[i]
    clear_keys(f"{kind}_item_")  # индексы сдвинулись — сбрасываем виджеты
    commit()


def _render_traits(kind: str) -> None:
    title, icon, empty = TRAITS[kind]
    st.markdown(f'<div class="panel-title">{title}</div>', unsafe_allow_html=True)
    items = getattr(get_char(), kind)
    if not items:
        _empty(icon, empty)
    for i, text in enumerate(items):
        a, b = st.columns([6, 1])
        a.text_input(title, value=text, key=f"{kind}_item_{i}", label_visibility="collapsed",
                     on_change=_edit_trait, args=(kind, i))
        b.button("🗑", key=f"del_{kind}_{i}", on_click=_del_trait, args=(kind, i))
    with st.form(f"{kind}_form", clear_on_submit=True, border=False):
        st.text_input("Новая строка", key=f"{kind}_new", placeholder="+ добавить…")
        st.form_submit_button("＋ Добавить", on_click=_add_trait, args=(kind,))


def render() -> None:
    left, right = st.columns(2)
    with left:
        _render_effects("buffs")
    with right:
        _render_effects("debuffs")
    left, right = st.columns(2)
    with left:
        _render_traits("strengths")
    with right:
        _render_traits("weaknesses")
