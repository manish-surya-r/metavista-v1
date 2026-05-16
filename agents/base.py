from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass(frozen=True)
class AgentSpec:
    id: str
    name: str
    icon: str
    description: str
    activation_keywords: tuple[str, ...]
    system_prompt: str
    mock_runner: Callable[[str, str, str, str], str]
    # Optional async runner that calls a real LLM via an OpenAICompatibleClient.
    # Signature: async (client, system_prompt, user_prompt) -> str
    llm_runner: Callable | None = None


@dataclass
class AgentOutput:
    agent_id: str
    name: str
    icon: str
    content: str
    model_used: str = "local"
