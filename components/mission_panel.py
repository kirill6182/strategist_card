import streamlit as st

from storage import commit, get_char


def _save(attr: str) -> None:
    setattr(get_char().mission, attr, st.session_state[f"mission_{attr}"].strip())
    commit()


def render() -> None:
    m = get_char().mission
    st.markdown('<div class="panel-title">🎯 Текущая миссия</div>', unsafe_allow_html=True)
    st.text_area("Цель", value=m.goal, key="mission_goal", height=80,
                 on_change=_save, args=("goal",), placeholder="Чего я хочу добиться?")
    a, b = st.columns(2)
    a.text_input("✔️ Критерий «выполнено»", value=m.success_criteria, key="mission_success_criteria",
                 on_change=_save, args=("success_criteria",), placeholder="Как я пойму, что готово?")
    b.text_input("🏆 Награда", value=m.reward, key="mission_reward",
                 on_change=_save, args=("reward",), placeholder="Чем отмечу победу?")
