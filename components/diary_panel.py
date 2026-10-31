import html
from datetime import date

import streamlit as st

from models import DiaryEntry, new_id
from storage import commit, get_char


def _add_entry() -> None:
    ss, char = st.session_state, get_char()
    event = ss.diary_event.strip()
    if not event:
        st.toast("Опиши событие", icon="⚠️")
        return
    delta_text = "—"
    stat = next((s for s in char.stats if s.id == ss.diary_stat), None)
    if stat and ss.diary_delta != 0:
        delta_text = f"{stat.name} {ss.diary_delta:+d}"
        if ss.diary_apply:
            stat.value = max(1, min(10, stat.value + ss.diary_delta))
    char.diary.append(DiaryEntry(new_id(), ss.diary_date.isoformat(), event, delta_text,
                                 ss.diary_effect.strip()))
    commit()


def _del_entry() -> None:
    char = get_char()
    char.diary[:] = [d for d in char.diary if d.id != st.session_state.diary_del]
    commit()


def render() -> None:
    char = get_char()
    st.markdown('<div class="panel-title">📅 Дневник стратега</div>', unsafe_allow_html=True)
    if char.diary:
        rows = "".join(
            f"<tr><td class='mono'>{html.escape(d.date)}</td><td>{html.escape(d.event)}</td>"
            f"<td class='mono'>{html.escape(d.stat_delta)}</td><td>{html.escape(d.effect)}</td></tr>"
            for d in sorted(char.diary, key=lambda d: d.date, reverse=True))
        st.markdown("<div class='dl'><table class='diary'><tr><th>Дата</th><th>Событие</th>"
                    f"<th>Стат ±</th><th>Бафф / дебафф</th></tr>{rows}</table></div>",
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty"><span class="ico">📜</span>Запиши первое событие</div>',
                    unsafe_allow_html=True)

    with st.form("diary_form", clear_on_submit=True):
        a, b = st.columns([1, 3])
        a.date_input("Дата", value=date.today(), key="diary_date")
        b.text_input("Событие (от третьего лица)", key="diary_event",
                     placeholder="Персонаж столкнулся с…")
        c, d, e = st.columns([2, 1, 2])
        c.selectbox("Стат", ["—"] + [s.id for s in char.stats], key="diary_stat",
                    format_func=lambda i: "—" if i == "—" else next(
                        f"{s.icon} {s.name}" for s in char.stats if s.id == i))
        d.number_input("±", min_value=-3, max_value=3, value=0, step=1, key="diary_delta")
        e.text_input("Бафф / дебафф", key="diary_effect")
        st.checkbox("Применить изменение к стату", value=True, key="diary_apply")
        st.form_submit_button("＋ Записать", on_click=_add_entry)

    if char.diary:
        with st.expander("🗑 Удалить запись"):
            st.selectbox("Запись", [d.id for d in char.diary], key="diary_del",
                         format_func=lambda i: next(f"{d.date} — {d.event[:50]}"
                                                    for d in char.diary if d.id == i))
            st.button("Удалить", on_click=_del_entry, key="diary_del_btn")
