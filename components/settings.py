"""SettingsModal (сброс к демо) и блок бэкапа (экспорт/импорт JSON)."""
import json
from datetime import date

import streamlit as st

from demo import demo_character
from models import Character
from storage import DATA_FILE, get_char, replace_char


@st.dialog("⚙️ Настройки")
def settings_dialog() -> None:
    st.caption(f"Данные хранятся в файле: `{DATA_FILE}`")
    st.warning("Сброс удалит текущего персонажа и вернёт демо-данные.")
    ok = st.checkbox("Я понимаю, что действие необратимо", key="reset_confirm")
    if st.button("Сбросить к демо-данным", type="primary", disabled=not ok):
        replace_char(demo_character())
        st.rerun()


def render_backup() -> None:
    st.markdown('<div class="panel-title">💾 Резервная копия</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    a.download_button("⬇️ Экспорт JSON",
                      data=json.dumps(get_char().to_dict(), ensure_ascii=False, indent=2),
                      file_name=f"strategist_{date.today().isoformat()}.json",
                      mime="application/json")
    with b.popover("⬆️ Импорт JSON"):
        up = st.file_uploader("Файл бэкапа", type="json", key="import_file")
        if up is not None and st.button("Применить импорт", key="import_apply"):
            try:
                new = Character.from_dict(json.loads(up.getvalue().decode("utf-8")))
            except (ValueError, UnicodeDecodeError) as exc:
                st.error(f"Не удалось импортировать: {exc}")
            else:
                replace_char(new)
                st.rerun()
