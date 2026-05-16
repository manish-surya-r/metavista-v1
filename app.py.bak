import time
import uuid
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MetaVista",
    page_icon="MV",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f8fb;
    color: #111827;
}

.block-container {
    padding-top: 2rem;
    max-width: 1220px;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    padding: 40px;
    border-radius: 28px;
    background: linear-gradient(135deg, #ffffff 0%, #eef4ff 100%);
    border: 1px solid #dbe3ef;
    box-shadow: 0 20px 60px rgba(15,23,42,0.08);
    margin-bottom: 24px;
}

.badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: #e0ecff;
    color: #1d4ed8;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 16px;
}

.hero h1 {
    font-size: 56px;
    line-height: 1;
    letter-spacing: -2px;
    margin: 0 0 12px 0;
    color: #0f172a;
}

.hero p {
    color: #475569;
    font-size: 18px;
    max-width: 780px;
}

.panel, .agent-card, .metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    box-shadow: 0 16px 40px rgba(15,23,42,0.06);
}

.panel {
    padding: 24px;
    margin-bottom: 18px;
}

.agent-card {
    padding: 22px;
    min-height: 150px;
    transition: all 0.2s ease;
}

.agent-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 50px rgba(15,23,42,0.10);
}

.agent-icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #eff6ff;
    color: #2563eb;
    font-weight: 800;
    margin-bottom: 14px;
}

.agent-title {
    font-size: 17px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 7px;
}

.agent-copy {
    color: #475569;
    font-size: 14px;
    line-height: 1.6;
}

.report-card {
    padding: 30px;
    border-radius: 24px;
    background: #ffffff;
    color: #111827;
    border: 1px solid #e2e8f0;
    box-shadow: 0 18px 50px rgba(15,23,42,0.07);
}

.report-card h1, .report-card h2, .report-card h3 {
    color: #0f172a;
}

.report-card p, .report-card li {
    color: #334155;
    line-height: 1.7;
}

.stTextArea textarea {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 18px !important;
    min-height: 180px !important;
}

.stTextArea label {
    color: #0f172a !important;
    font-weight: 800 !important;
}

.stButton > button {
    height: 52px;
    border-radius: 14px;
    font-weight: 800;
    border: none;
    background: #2563eb !important;
    color: white !important;
    box-shadow: 0 12px 25px rgba(37,99,235,0.24);
}

.stButton > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-1px);
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 18px;
    border-radius: 20px;
    box-shadow: 0 12px 32px rgba(15,23,42,0.06);
}

[data-testid="stMetricLabel"] {
    color: #64748b;
}

[data-testid="stMetricValue"] {
    color: #0f172a;
}

.stTabs [data-baseweb="tab"] {
    background: #ffffff;
    border-radius: 12px;
    color: #334155;
    padding: 10px 16px;
    border: 1px solid #e2e8f0;
}

.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    color: white !important;
}

hr {
    border-color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


def run_expansive_optimist(user_prompt: str) -> str:
    return f"""
### Expansive Optimist Brief

The question is:

{user_prompt}

Key findings:
- Social media algorithms optimize for attention and engagement.
- Adolescents are highly sensitive to reward loops.
- Infinite scroll and short videos encourage rapid attention switching.
- Personalized feeds increase compulsive engagement.
"""


def run_defensive_skeptic(user_prompt: str) -> str:
    return """
### Defensive Skeptic Brief

Important cautions:
- Correlation does not always imply causation.
- Attention span is difficult to measure precisely.
- Other variables like sleep and stress matter.
- Strong claims should be framed carefully.
"""


def run_peer_review(optimist: str, skeptic: str) -> dict:
    return {
        "cycle": 1,
        "consensus_count": 5,
        "conflict_count": 2,
        "log_summary": "Peer review completed.",
        "critique_text": """
Consensus:
- Algorithms influence engagement patterns.
- Infinite scroll affects attention behavior.

Conflicts:
- Degree of long-term impact remains uncertain.
"""
    }


def run_master_synthesis(user_prompt: str, optimist: str, skeptic: str, review: dict) -> str:
    return f"""
# MetaVista Verified Research Report

## 1. Executive Summary

Algorithmic social media may encourage rapid attentional switching in adolescents. The most careful conclusion is not that algorithms directly destroy attention, but that repeated exposure to fast, personalized, reward-driven feeds can train patterns of frequent context switching.

## 2. Comprehensive Deep Dive

Main structural contributors:

- Infinite scroll removes natural stopping points.
- Short-form video compresses attention into rapid cycles.
- Autoplay reduces deliberate choice.
- Personalized recommendation systems keep content emotionally relevant.
- Notifications interrupt offline attention.
- Likes, comments, and views convert attention into social feedback.

## 3. Audit Trail

### Optimist
{optimist}

### Skeptic
{skeptic}

### Peer Review
{review["critique_text"]}

## 4. Final Recommendation

Use careful evidence-aware framing while discussing psychological impacts.
"""


def run_metavista_audit(user_prompt: str) -> dict:
    session_id = f"mv-session-{uuid.uuid4().hex[:8]}"
    optimist = run_expansive_optimist(user_prompt)
    skeptic = run_defensive_skeptic(user_prompt)
    review = run_peer_review(optimist, skeptic)
    final_report = run_master_synthesis(user_prompt, optimist, skeptic, review)

    history = [
        {"cycle": 1, "consensus_count": 2, "conflict_count": 4, "log_summary": "Discovery found mechanisms and uncertainty."},
        {"cycle": 2, "consensus_count": 4, "conflict_count": 2, "log_summary": "Peer review rejected overstrong causal claims."},
        {"cycle": 3, "consensus_count": 6, "conflict_count": 0, "log_summary": "Final synthesis resolved conflicts."}
    ]

    return {
        "session_id": session_id,
        "user_prompt": user_prompt,
        "optimist": optimist,
        "skeptic": skeptic,
        "peer_review": review,
        "history": history,
        "final_report": {"title": "MetaVista Verified Research Report", "content": final_report, "links": []}
    }


def card(icon, title, copy):
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-icon">{icon}</div>
        <div class="agent-title">{title}</div>
        <div class="agent-copy">{copy}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    st.markdown("""
    <div class="hero">
        <div class="badge">MetaVista MVP</div>
        <h1>Reasoning Audit Engine</h1>
        <p>
            A professional multi-agent system that compares optimistic discovery,
            skeptical review, peer critique, and final synthesis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("01", "Optimist", "Expands the idea and gathers strong solution paths.")
    with c2:
        card("02", "Skeptic", "Checks assumptions, risks, and weak claims.")
    with c3:
        card("03", "Peer Review", "Compares consensus and conflict.")
    with c4:
        card("04", "Synthesis", "Creates a verified final report.")

    st.write("")

    left, right = st.columns([1.7, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        prompt = st.text_area(
            "Research Question",
            placeholder="Example: How does algorithmic social media affect adolescent attention?",
            height=180
        )
        run = st.button("Run Audit", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel">
            <h3 style="color:#0f172a; margin-top:0;">System Status</h3>
            <p style="color:#475569; line-height:1.7;">
                Local MVP mode is active. The UI is stable and ready for reconnecting
                Qwen, Z.ai, and TokenRouter.
            </p>
        </div>
        """, unsafe_allow_html=True)

    if run:
        if not prompt.strip():
            st.warning("Please enter a research question.")
            return

        progress = st.progress(0, text="Initializing audit...")
        for label, value in [
            ("Running Optimist Agent...", 25),
            ("Running Skeptic Agent...", 50),
            ("Running Peer Review...", 75),
            ("Generating Final Report...", 100),
        ]:
            time.sleep(0.35)
            progress.progress(value, text=label)

        session = run_metavista_audit(prompt.strip())
        df = pd.DataFrame(session["history"])

        st.success("Audit completed.")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Cycles", len(df))
        m2.metric("Consensus", int(df.iloc[-1]["consensus_count"]))
        m3.metric("Conflicts", int(df.iloc[-1]["conflict_count"]))
        m4.metric("Session", session["session_id"][-8:])

        st.markdown("---")

        report_col, telemetry_col = st.columns([1.6, 1])

        with report_col:
            st.markdown("## Final Verified Report")
            st.markdown(
                f'<div class="report-card">{session["final_report"]["content"]}</div>',
                unsafe_allow_html=True
            )

        with telemetry_col:
            st.markdown("## Audit Telemetry")
            chart_df = df.set_index("cycle")[["consensus_count", "conflict_count"]]
            st.line_chart(chart_df)
            st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("## Agent Audit Trail")
        tab1, tab2, tab3, tab4 = st.tabs(["Optimist", "Skeptic", "Peer Review", "Raw JSON"])

        with tab1:
            st.markdown(session["optimist"])
        with tab2:
            st.markdown(session["skeptic"])
        with tab3:
            st.markdown(session["peer_review"]["critique_text"])
        with tab4:
            st.json(session)


if __name__ == "__main__":
    main()
