from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class AgentSpec:
    id: str
    name: str
    icon: str
    description: str
    activation_keywords: tuple[str, ...]
    system_prompt: str
    mock_runner: Callable[[str, str, str, str], str]

@dataclass
class AgentOutput:
    agent_id: str
    name: str
    icon: str
    content: str
    model_used: str = "local"
