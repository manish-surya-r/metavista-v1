from pathlib import Path
import pandas as pd
import streamlit as st

from agents.registry import AGENT_REGISTRY
from core.workflow import run_audit_sync

st.set_page_config(
   page_title="MetaVista",
   page_icon="logo/logo.svg" if Path("logo/logo.svg").exists() else "🧭",
   layout="wide",
)

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top left, #eff6ff, #f8fafc 40%, white); }
.block-container { max-width: 1320px; padding-top: 1.4rem; }
.hero { padding: 42px; border-radius: 32px; background: linear-gradient(135deg,#fff,#eef4ff); border:1px solid #dbeafe; box-shadow:0 24px 70px rgba(15,23,42,.10); margin-bottom:22px; }
.hero h1 { font-size:56px; line-height:.95; letter-spacing:-2px; margin:0; color:#0f172a; }
.hero p { color:#475569; font-size:18px; line-height:1.7; max-width:900px; }
.panel,.card,.report { background:white; border:1px solid #e2e8f0; border-radius:24px; box-shadow:0 16px 45px rgba(15,23,42,.07); padding:24px; }
.card { min-height:150px; margin-bottom:14px; }
.icon { width:42px; height:42px; border-radius:14px; background:#eff6ff; color:#2563eb; display:flex; align-items:center; justify-content:center; font-weight:900; margin-bottom:10px; }
.title { font-weight:900; color:#0f172a; }
.copy { color:#64748b; font-size:13px; line-height:1.55; }
.stButton button { height:54px; border-radius:16px; font-weight:900; background:#2563eb !important; color:white !important; border:0 !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
   st.image("logo/logo.svg", width=90)
   st.header("MetaVista")
   st.write("Multi-agent research engine.")
   st.divider()
   st.write("Add future agents in:")
   st.code("agents/registry.py")

st.markdown("""
<div class="hero">
<h1>Advanced research, routed through specialist agents.</h1>
<p>Enter a prompt, optionally define the topic and acting lens, choose the research depth, and MetaVista activates specialist agents for extraction, references, tables, visuals, skeptical review, and final synthesis.</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(3)
for i, agent in enumerate(AGENT_REGISTRY.values()):
   with cols[i % 3]:
       st.markdown(f"""
       <div class="card">
           <div class="icon">{agent.icon}</div>
           <div class="title">{agent.name}</div>
           <div class="copy">{agent.description}</div>
       </div>
       """, unsafe_allow_html=True)

left, right = st.columns([1.7, 1])

with left:
   st.markdown('<div class="panel">', unsafe_allow_html=True)
   topic = st.text_input("Topic / Research Area", placeholder="Optional")
   acting_lens = st.text_input("Acting Lens / Expert Role", placeholder="Optional: senior AI architect, advisor, developer...")
   prompt = st.text_area("Prompt *", placeholder="Only this field is mandatory.")
   c1, c2 = st.columns(2)
   with c1:
       depth = st.selectbox("Research Depth", ["Basic Research", "Medium Research", "Deep Research"], index=1)
   with c2:
       generate_pdf = st.toggle("Generate downloadable PDF", value=True)
   run = st.button("Run Multi-Agent Research", use_container_width=True)
   st.markdown("</div>", unsafe_allow_html=True)

with right:
   st.markdown("""
   <div class="panel">
   <h3>Workflow</h3>
   <ol>
   <li>Assess prompt</li>
   <li>Activate relevant agents</li>
   <li>Collect specialist outputs</li>
   <li>Review assumptions</li>
   <li>Synthesize report</li>
   <li>Export PDF</li>
   </ol>
   </div>
   """, unsafe_allow_html=True)

if run:
   if not prompt.strip():
       st.warning("Please enter a prompt.")
       st.stop()

   session = run_audit_sync(topic.strip(), acting_lens.strip(), prompt.strip(), depth, generate_pdf)

   st.success("Multi-agent research completed.")

   m1, m2, m3 = st.columns(3)
   m1.metric("Activated Agents", len(session.activated_agents))
   m2.metric("Research Depth", depth.replace(" Research", ""))
   m3.metric("Session", session.session_id)

   df = pd.DataFrame([x.__dict__ for x in session.history])

   report_col, audit_col = st.columns([1.5, 1])

   with report_col:
       st.subheader("Final Advanced Report")
       st.markdown('<div class="report">', unsafe_allow_html=True)
       st.markdown(session.final_report.content)
       st.markdown("</div>", unsafe_allow_html=True)

       if session.final_report.pdf_path and Path(session.final_report.pdf_path).exists():
           st.download_button(
               "Download Detailed PDF Report",
               data=Path(session.final_report.pdf_path).read_bytes(),
               file_name=Path(session.final_report.pdf_path).name,
               mime="application/pdf",
               use_container_width=True,
           )

   with audit_col:
       st.subheader("Audit Telemetry")
       st.line_chart(df.set_index("cycle")[["consensus_count", "conflict_count"]])
       st.dataframe(df, use_container_width=True, hide_index=True)

   st.subheader("Specialist Agent Outputs")
   tabs = st.tabs([x.name for x in session.agent_outputs])
   for tab, output in zip(tabs, session.agent_outputs):
       with tab:
           st.markdown(output.content)
