from __future__ import annotations

import asyncio

from .base import AgentOutput
from .registry import select_agents
from core.router import ModelRouter


def _build_user_prompt(topic: str, role: str, prompt: str, depth: str) -> str:
    """Combine context fields into a single user prompt for the LLM."""
    parts = []
    if topic:
        parts.append(f'Topic: {topic}')
    if role:
        parts.append(f'Acting Lens: {role}')
    parts.append(f'Research Depth: {depth}')
    parts.append(f'Prompt: {prompt}')
    return '\n'.join(parts)


def run_multi_agent_research(topic: str, role: str, prompt: str, depth: str):
    """Run selected agents with real LLM clients or mock fallback.

    When real API keys are available, calls the LLM via the agent's
    llm_runner. Otherwise falls back to the synchronous mock_runner.
    """
    router = ModelRouter()
    selected = select_agents(f'{topic}\n{role}\n{prompt}', depth)
    user_prompt = _build_user_prompt(topic, role, prompt, depth)

    async def _run_one(agent):
        client = router.default_client()
        is_real = not router.is_mock and agent.llm_runner is not None

        if is_real:
            try:
                content = await agent.llm_runner(client, agent.system_prompt, user_prompt)
                return AgentOutput(
                    agent_id=agent.id,
                    name=agent.name,
                    icon=agent.icon,
                    content=content,
                    model_used=client.model,
                )
            except Exception:
                # LLM call failed – fall back to mock
                pass

        # Mock path (no API key, no llm_runner, or LLM error)
        content = agent.mock_runner(topic, role, prompt, depth)
        return AgentOutput(
            agent_id=agent.id,
            name=agent.name,
            icon=agent.icon,
            content=content,
            model_used='mock',
        )

    # Run all agents concurrently
    async def _run_all():
        return list(await asyncio.gather(*[_run_one(a) for a in selected]))

    outputs = asyncio.run(_run_all())
    return list(selected), outputs
