from types import SimpleNamespace

from core.prompts import (
    OPTIMIST_PROMPT,
    SKEPTIC_PROMPT,
    PEER_REVIEW_PROMPT,
    SYNTHESIS_PROMPT
)


async def run_expansive_optimist(user_prompt: str, client=None, mock: bool = True):
    content = f"""
# Expansive Optimist Report

The system explored broad solution pathways for:

{user_prompt}

Key opportunities:
- scalable architecture
- modular AI orchestration
- distributed reasoning
- model specialization
- audit transparency

Detailed Analysis:
{OPTIMIST_PROMPT.format(USER_PROMPT=user_prompt)}
"""
    return SimpleNamespace(content=content)


async def run_defensive_skeptic(user_prompt: str, client=None, mock: bool = True):
    content = f"""
# Defensive Skeptic Report

Potential concerns:
- hallucination risk
- scaling bottlenecks
- API dependency
- latency constraints
- cost explosion in multi-agent loops

Detailed Analysis:
{SKEPTIC_PROMPT.format(USER_PROMPT=user_prompt)}
"""
    return SimpleNamespace(content=content)


async def run_peer_review(user_prompt: str, brief_a: str, brief_b: str, client=None, mock: bool = True):
    content = """
Consensus:
- modular systems are beneficial
- multiple agents improve robustness

Conflicts:
- cost vs quality tradeoff
- latency vs depth of reasoning
"""
    return SimpleNamespace(
        content=content,
        consensus_count=4,
        conflict_count=2,
        critique_text=content
    )


async def run_master_synthesizer(
    user_prompt: str,
    brief_a: str,
    brief_b: str,
    critique: str,
    client=None,
    mock: bool = True
):
    content = f"""
# MetaVista Verified Research Report

## 1. Executive Summary

MetaVista successfully completed a multi-agent audit for:

{user_prompt}

## 2. Comprehensive Deep Dive

### Expansive Optimist Findings
{brief_a}

### Defensive Skeptic Findings
{brief_b}

## 3. Audit Trail

{critique}

## 4. Final Recommendation

Use:
- Streamlit frontend
- async orchestration
- model specialization
- audit transparency
- lightweight modular architecture

The MVP architecture is validated.
"""
    return SimpleNamespace(content=content)
