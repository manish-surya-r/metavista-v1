"""Mock LLM client for development and testing without real API keys.

Drop-in replacement for OpenAICompatibleClient. Returns deterministic
mock responses based on the system prompt content, so different agents
in the MetaVista pipeline receive context-appropriate output.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)


class MockClient:
    """Mock LLM client that returns canned responses.

    Implements the same public interface as OpenAICompatibleClient:
        - chat(system_prompt, user_prompt, temperature) -> str
        - ping() -> bool
        - is_configured -> bool
    """

    def __init__(
        self,
        provider_name: str = 'Mock',
        latency_ms: int = 0,
    ):
        self.provider_name = provider_name
        self.api_key = 'mock-key'
        self.model = 'mock-model'
        self.base_url = 'https://mock.local'
        self.latency_ms = latency_ms

    # -- properties ----------------------------------------------------------

    @property
    def is_configured(self) -> bool:
        """Always True – mock client is always ready."""
        return True

    # -- public API ----------------------------------------------------------

    async def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.25) -> str:
        """Return a mock response appropriate to the agent role.

        The system prompt is inspected for keywords to determine which
        canned response to return. Falls back to a generic response.
        """
        if self.latency_ms:
            await asyncio.sleep(self.latency_ms / 1000.0)

        prompt_lower = system_prompt.lower()

        if 'optimist' in prompt_lower:
            return self._mock_optimist(user_prompt)
        if 'skeptic' in prompt_lower:
            return self._mock_skeptic(user_prompt)
        if 'peer review' in prompt_lower or 'peer_review' in prompt_lower:
            return self._mock_peer_review(user_prompt)
        if 'synthes' in prompt_lower:
            return self._mock_synthesis(user_prompt)

        # Generic fallback
        logger.debug('[%s] No role detected in system prompt, returning generic mock', self.provider_name)
        return f'Mock response for: {user_prompt[:80]}'

    async def ping(self) -> bool:
        """Always returns True – mock client is always reachable."""
        return True

    # -- private helpers -----------------------------------------------------

    @staticmethod
    def _mock_optimist(user_prompt: str) -> str:
        return f"""# Expansive Optimist Brief

The system explored broad solution pathways for:

{user_prompt}

Key opportunities:
- Scalable architecture with modular components
- Distributed reasoning across specialized agents
- Model specialization improves output quality
- Audit transparency builds user trust
- Lightweight MVP approach reduces risk

Detailed Analysis:
This is a mock optimist response. In production, the Qwen/TokenRouter
endpoint would generate a full research brief here.
"""

    @staticmethod
    def _mock_skeptic(user_prompt: str) -> str:
        return f"""# Defensive Skeptic Brief

Potential concerns for:

{user_prompt}

Key risks:
- Hallucination risk in generated content
- Scaling bottlenecks under concurrent load
- API dependency creates single points of failure
- Latency constraints in multi-agent loops
- Cost explosion without careful token budgeting

Detailed Analysis:
This is a mock skeptic response. In production, the Qwen/TokenRouter
endpoint would generate a full risk-audit brief here.
"""

    @staticmethod
    def _mock_peer_review(user_prompt: str) -> str:
        return """Consensus:
- Modular systems are broadly beneficial
- Multiple agents improve robustness and coverage
- Audit trails increase credibility

Conflicts:
- Cost vs. quality tradeoff remains unresolved
- Latency vs. depth of reasoning is context-dependent

Blind spots:
- Long-term maintenance of multi-agent pipelines
- Evaluation metrics for synthesis quality

Critique summary:
Both briefs agree on the value of modular, multi-agent architectures.
The optimist underestimates operational cost; the skeptic underestimates
user-facing value. A balanced approach is recommended.
"""

    @staticmethod
    def _mock_synthesis(user_prompt: str) -> str:
        return f"""# MetaVista Verified Research Report

## 1. Executive Summary

MetaVista successfully completed a multi-agent audit for:

{user_prompt}

The analysis combined expansive discovery with skeptical risk assessment,
mediated by peer review, to produce a balanced, verified conclusion.

## 2. Comprehensive Deep Dive

### Key Findings
- Modular multi-agent architecture is validated
- Cost-quality tradeoffs require careful monitoring
- Audit transparency improves user confidence

### Risks Identified
- API dependency and rate limit constraints
- Latency in sequential agent pipelines
- Token cost management at scale

## 3. Audit Trail

Peer review identified 3 consensus points and 2 conflicts.
Conflicts were resolved or explicitly preserved as caveats.

## 4. Final Recommendation

Adopt a lightweight, modular architecture with:
- Async orchestration for parallel agent execution
- Model specialization per agent role
- Built-in audit logging for transparency
- Token budgeting and fallback strategies

This is a mock synthesis. In production, the Z.ai endpoint would
generate the full verified report here.
"""
