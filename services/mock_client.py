"""Mock LLM client for development and testing without real API keys.

Drop-in replacement for OpenAICompatibleClient. Returns deterministic
mock responses based on the system prompt content, so different agents
in the MetaVista pipeline receive context-appropriate output.
"""

from __future__ import annotations

import asyncio
import logging

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
        if 'extract' in prompt_lower:
            return self._mock_extractor(user_prompt)
        if 'reference' in prompt_lower or 'evidence' in prompt_lower:
            return self._mock_reference(user_prompt)
        if 'table' in prompt_lower or 'compar' in prompt_lower:
            return self._mock_table(user_prompt)
        if 'visual' in prompt_lower or 'graph' in prompt_lower:
            return self._mock_visual(user_prompt)

        # Generic fallback
        logger.debug('[%s] No role detected in system prompt, returning generic mock', self.provider_name)
        return f'Mock response for: {user_prompt[:80]}'

    def chat_sync(self, system_prompt: str, user_prompt: str, temperature: float = 0.25) -> str:
        """Synchronous version of chat() for use in non-async contexts."""
        prompt_lower = system_prompt.lower()

        if 'optimist' in prompt_lower:
            return self._mock_optimist(user_prompt)
        if 'skeptic' in prompt_lower:
            return self._mock_skeptic(user_prompt)
        if 'peer review' in prompt_lower or 'peer_review' in prompt_lower:
            return self._mock_peer_review(user_prompt)
        if 'synthes' in prompt_lower:
            return self._mock_synthesis(user_prompt)
        if 'extract' in prompt_lower:
            return self._mock_extractor(user_prompt)
        if 'reference' in prompt_lower or 'evidence' in prompt_lower:
            return self._mock_reference(user_prompt)
        if 'table' in prompt_lower or 'compar' in prompt_lower:
            return self._mock_table(user_prompt)
        if 'visual' in prompt_lower or 'graph' in prompt_lower:
            return self._mock_visual(user_prompt)

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

Critique summary:
Both briefs agree on the value of modular, multi-agent architectures.
A balanced approach is recommended.
"""

    @staticmethod
    def _mock_synthesis(user_prompt: str) -> str:
        return f"""# MetaVista Verified Research Report

## 1. Executive Summary

MetaVista successfully completed a multi-agent audit for:

{user_prompt}

The analysis combined expansive discovery with skeptical risk assessment,
mediated by peer review, to produce a balanced, verified conclusion.

## 2. Key Findings
- Modular multi-agent architecture is validated
- Cost-quality tradeoffs require careful monitoring
- Audit transparency improves user confidence

## 3. Final Recommendation
Adopt a lightweight, modular architecture with async orchestration
and built-in audit logging.

This is a mock synthesis. In production, the Z.ai endpoint would
generate the full verified report here.
"""

    @staticmethod
    def _mock_extractor(user_prompt: str) -> str:
        return f"""## Information Extraction Agent

### Extracted Task
- Main request: {user_prompt}
- Required output: advanced research-style answer
- Needs: structure, evidence awareness, recommendations, and final report readiness.

### Decomposition
1. Understand the task.
2. Identify facts, assumptions, constraints, and expected outputs.
3. Separate evidence-backed claims from reasoning.
4. Prepare clean sections for synthesis.
"""

    @staticmethod
    def _mock_reference(user_prompt: str) -> str:
        return """## Reference and Evidence Agent

### Evidence Strategy
- Prefer official docs, primary sources, research papers, and credible technical references.
- Mark unsupported claims clearly.
- Use citations for current facts, laws, prices, model specs, and benchmarks.
- Separate verified evidence from assumptions.

### Citation Plan
| Claim Type | Source Type | Rule |
|---|---|---|
| Definition | official docs/textbook | cite once |
| Current fact | recent web source | cite every claim |
| Technical claim | docs/paper | cite version/date |
| Recommendation | source + reasoning | state assumptions |
"""

    @staticmethod
    def _mock_table(user_prompt: str) -> str:
        return """## Tables and Comparison Agent

### Suggested Tables
| Table | Purpose |
|---|---|
| Agent activation matrix | shows which agents were used and why |
| Evidence quality matrix | separates strong and weak claims |
| Risk table | exposes uncertainty and mitigations |
| Recommendation table | converts research into decisions |
"""

    @staticmethod
    def _mock_visual(user_prompt: str) -> str:
        return """## Visuals and Graph Agent

### Visual Recommendations
- Workflow diagram: prompt → router → agents → synthesis → PDF.
- Agent contribution chart.
- Conflict/consensus telemetry chart.
- Tables or diagrams only when they clarify the answer.
"""
