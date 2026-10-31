"""Карточка персонажа-стратега — точка входа (streamlit run app.py)."""
import streamlit as st

from components import diary_panel, effects_panel, header, mission_panel, settings, stats_panel
from storage import get_char
from styles import CSS

st.set_page_config(page_title="Карточка стратега", page_icon="♟️", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

get_char()  # загрузка из файла или демо-данные при первом запуске
header.render()
stats_panel.render()
effects_panel.render()
mission_panel.render()
diary_panel.render()
settings.render_backup()
