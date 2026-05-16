from dataclasses import dataclass
from pathlib import Path
import json
import time

from agents import run_multi_agent_research
from core.reporting import build_pdf_report

@dataclass
class AuditCycle:
    cycle: int
    consensus_count: int
    conflict_count: int
    log_summary: str

@dataclass
class FinalReport:
    title: str
    content: str
    pdf_path: str | None = None

@dataclass
class MetaVistaSession:
    session_id: str
    topic: str
    acting_lens: str
    research_depth: str
    user_prompt: str
    activated_agents: list[str]
    history: list[AuditCycle]
    final_report: FinalReport
    agent_outputs: list

def _compose_report(topic, acting_lens, prompt, depth, outputs):
    sections = "\n\n".join([f"### {o.icon} {o.name}\n{o.content}" for o in outputs])
    return f"""# MetaVista Advanced Research Report

## Executive Summary
This report was generated through a modular multi-agent workflow. The system assessed the prompt, activated relevant specialist agents, collected outputs, reviewed risks, and synthesized a detailed research-style answer.

**Topic:** {topic or "Not provided"}  
**Acting Lens:** {acting_lens or "Neutral expert advisor"}  
**Research Depth:** {depth}

## User Prompt
{prompt}

## Activated Workflow
1. Assess the prompt.
2. Select relevant agents.
3. Run specialist agents.
4. Review assumptions and evidence gaps.
5. Synthesize final report.
6. Generate downloadable PDF if enabled.

## Specialist Findings
{sections}

## Final Recommendation
Keep the system registry-based. Each new agent should be added inside `agents/registry.py` with an ID, name, keywords, system prompt, and runner. The orchestrator should only select and call registered agents so future expansion remains simple.

## Caveats
This implementation gives you the architecture and UI flow. For production-grade references, connect the Reference Agent to live web search, PDFs, papers, or internal document stores.
"""

def run_audit_sync(topic, acting_lens, user_prompt, research_depth, generate_pdf=False):
    selected, outputs = run_multi_agent_research(topic, acting_lens, user_prompt, research_depth)
    content = _compose_report(topic, acting_lens, user_prompt, research_depth, outputs)
    pdf_path = build_pdf_report("MetaVista Advanced Research Report", content) if generate_pdf else None

    history = [
        AuditCycle(1, 2, 3, "Router assessed prompt and selected agents."),
        AuditCycle(2, len(outputs), 2, "Specialist agents produced outputs."),
        AuditCycle(3, len(outputs) + 2, 0, "Final synthesis consolidated the report."),
    ]

    session = MetaVistaSession(
        session_id=f"mv-{int(time.time())}",
        topic=topic,
        acting_lens=acting_lens,
        research_depth=research_depth,
        user_prompt=user_prompt,
        activated_agents=[a.name for a in selected],
        history=history,
        final_report=FinalReport("MetaVista Advanced Research Report", content, pdf_path),
        agent_outputs=outputs,
    )

    Path("data").mkdir(exist_ok=True)
    Path("data/last_session.json").write_text(json.dumps({
        "session_id": session.session_id,
        "topic": topic,
        "acting_lens": acting_lens,
        "research_depth": research_depth,
        "user_prompt": user_prompt,
        "activated_agents": session.activated_agents,
        "final_report": content,
        "pdf_path": pdf_path,
    }, indent=2))

    return session
