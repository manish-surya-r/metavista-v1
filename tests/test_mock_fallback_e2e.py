"""End-to-end tests: MockClient, router fallback, and full audit pipeline."""

import time

import pytest

from config.settings import Settings
from core.router import ModelRouter
from services.mock_client import MockClient
from services.qwen_client import QwenClient
from services.zai_client import ZaiClient


# ---------------------------------------------------------------------------
# Helper – Settings with no API keys (pure mock mode)
# ---------------------------------------------------------------------------

def _mock_settings() -> Settings:
    return Settings(_env_file=None)


# ---------------------------------------------------------------------------
# MockClient
# ---------------------------------------------------------------------------

def test_mock_client_is_configured():
    c = MockClient()
    assert c.is_configured is True


@pytest.mark.asyncio
async def test_mock_client_ping():
    c = MockClient()
    assert await c.ping() is True


@pytest.mark.asyncio
async def test_mock_client_chat_extractor():
    c = MockClient()
    result = await c.chat('You are an Information Extraction Agent.', 'test query')
    assert 'Extract' in result


@pytest.mark.asyncio
async def test_mock_client_chat_skeptic():
    c = MockClient()
    result = await c.chat('You are a Skeptical Review Agent.', 'test query')
    assert 'Skeptic' in result


@pytest.mark.asyncio
async def test_mock_client_chat_synthesizer():
    c = MockClient()
    result = await c.chat('You are the Master Synthesis Agent.', 'future of work')
    assert 'Research Report' in result


def test_mock_client_chat_sync():
    c = MockClient()
    result = c.chat_sync('You are an Information Extraction Agent.', 'test')
    assert 'Extract' in result


# ---------------------------------------------------------------------------
# ModelRouter fallback
# ---------------------------------------------------------------------------

def test_router_falls_back_to_mock_without_keys():
    s = _mock_settings()
    router = ModelRouter(s)
    assert isinstance(router.qwen, MockClient)
    assert isinstance(router.zai, MockClient)
    assert isinstance(router.critique_client(), MockClient)
    assert isinstance(router.synthesis_client(), MockClient)
    assert isinstance(router.default_client(), MockClient)
    assert router.is_mock is True


def test_router_uses_real_clients_with_keys():
    s = Settings(_env_file=None, QWEN_API_KEY='sk-test', ZAI_API_KEY='sk-test')
    router = ModelRouter(s)
    assert isinstance(router.qwen, QwenClient)
    assert isinstance(router.zai, ZaiClient)
    assert router.is_mock is False


# ---------------------------------------------------------------------------
# Full audit pipeline via new agents/ orchestrator
# ---------------------------------------------------------------------------

def test_full_audit_with_mock():
    """Run the entire audit pipeline with no real API keys.

    This exercises the new agents/ module → orchestrator → ModelRouter
    mock fallback → core/workflow.py path end-to-end.
    """
    from core.workflow import run_audit_sync

    session = run_audit_sync(
        topic='AI in Education',
        acting_lens='senior researcher',
        user_prompt='How does AI affect education?',
        research_depth='Medium Research',
        generate_pdf=False,
    )

    assert session.session_id.startswith('mv-')
    assert session.user_prompt == 'How does AI affect education?'
    assert len(session.activated_agents) >= 3  # extractor, skeptic, synthesizer at minimum
    assert len(session.agent_outputs) >= 3
    assert len(session.final_report.content) > 50
    # All outputs should have content (model_used depends on whether keys are present)
    for output in session.agent_outputs:
        assert len(output.content) > 0
        assert output.model_used in ('mock', 'qwen-plus', 'qwen-max', 'qwen-turbo', 'glm-4-plus', 'local-agent')


def test_full_audit_deep_research():
    """Deep research activates more agents."""
    from core.workflow import run_audit_sync

    session = run_audit_sync(
        topic='Technology',
        acting_lens='',
        user_prompt='Compare cloud providers',
        research_depth='Deep Research',
        generate_pdf=False,
    )
    # Deep research should activate extractor, skeptic, synthesizer + reference, table, visual
    assert len(session.activated_agents) >= 5


# ---------------------------------------------------------------------------
# Agent registry has llm_runner on all specs
# ---------------------------------------------------------------------------

def test_all_agents_have_llm_runner():
    from agents.registry import AGENT_REGISTRY
    for agent_id, spec in AGENT_REGISTRY.items():
        assert spec.llm_runner is not None, f'{agent_id} missing llm_runner'


def test_all_agents_have_rich_system_prompts():
    from agents.registry import AGENT_REGISTRY
    for agent_id, spec in AGENT_REGISTRY.items():
        assert len(spec.system_prompt) > 20, f'{agent_id} has a short system_prompt'
