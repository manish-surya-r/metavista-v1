from __future__ import annotations

import pandas as pd
import streamlit as st
from core.contracts import AuditCycle


def telemetry_dataframe(history: list[AuditCycle]) -> pd.DataFrame:
    return pd.DataFrame([h.model_dump() for h in history])


def render_telemetry(history: list[AuditCycle]) -> None:
    df = telemetry_dataframe(history)
    st.subheader('Audit Telemetry')
    st.dataframe(df, use_container_width=True, hide_index=True)

    chart_df = df.set_index('cycle')[['consensus_count', 'conflict_count']]
    st.line_chart(chart_df)
