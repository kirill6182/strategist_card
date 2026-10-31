import html

import streamlit as st

from storage import commit, get_char


def _shift(stat_id: str, delta: int) -> None:
    for s in get_char().stats:
        if s.id == stat_id:
            s.value = max(1, min(10, s.value + delta))  # валидация 1-10
    commit()


def _card(stat) -> str:
    segs = "".join(f'<span class="seg{" on" if i < stat.value else ""}"></span>' for i in range(10))
    tip = html.escape(stat.hint or "Растёт от осознанных действий", quote=True)
    return (f'<div class="stat-card tip" data-tip="{tip}"><div class="stat-top">'
            f'<span class="stat-name">{html.escape(stat.icon)} {html.escape(stat.name)}</span>'
            f'<span class="stat-val mono">{stat.value}<small>/10</small></span></div>'
            f'<div class="segs">{segs}</div></div>')


def render() -> None:
    st.markdown('<div class="panel-title">📊 Базовые статы</div>', unsafe_allow_html=True)
    stats = get_char().stats
    for row in range(0, len(stats), 3):
        cols = st.columns(3)
        for col, stat in zip(cols, stats[row:row + 3]):
            with col:
                st.markdown(_card(stat), unsafe_allow_html=True)
                m, p = st.columns(2)
                m.button("−", key=f"dec_{stat.id}", on_click=_shift, args=(stat.id, -1),
                         disabled=stat.value <= 1)
                p.button("+", key=f"inc_{stat.id}", on_click=_shift, args=(stat.id, 1),
                         disabled=stat.value >= 10)
