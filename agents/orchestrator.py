from .base import AgentOutput
from .registry import select_agents

def run_multi_agent_research(topic: str, role: str, prompt: str, depth: str):
    selected = select_agents(f"{topic}\n{role}\n{prompt}", depth)
    outputs = [
        AgentOutput(
            agent_id=a.id,
            name=a.name,
            icon=a.icon,
            content=a.mock_runner(topic, role, prompt, depth),
            model_used="local-agent"
        )
        for a in selected
    ]
    return selected, outputs
