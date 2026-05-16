from __future__ import annotations

import streamlit as st
from core.contracts import MetaVistaSession
from ui.charts import render_telemetry


def render_header() -> None:
    st.set_page_config(page_title='MetaVista', page_icon='🧭', layout='wide')
    st.title('🧭 MetaVista')
    st.caption('A multi-agent research and reasoning audit engine')


def render_sidebar() -> None:
    with st.sidebar:
        st.header('MetaVista MVP')
        st.write('Critique agents: Qwen Cloud or TokenRouter')
        st.write('Final synthesis: Z.ai / GLM')
        st.divider()
        st.info('If API keys are missing, the app automatically runs in mock mode.')


def render_session(session: MetaVistaSession) -> None:
    st.success(f'Audit complete: {session.session_id}')

    left, right = st.columns([2, 1])
    with left:
        st.subheader('Final Verified Report')
        st.markdown(session.final_report.content)
    with right:
        render_telemetry(session.history)

    st.divider()
    st.subheader('Audit Trail')
    for output in session.agent_outputs:
        with st.expander(f'{output.title} — model: {output.model_used}', expanded=False):
            st.markdown(output.content)
