"""Tests for services/mock_client.py – mock fallback client."""

import time

import pytest

from services.mock_client import MockClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client() -> MockClient:
    return MockClient()


# ---------------------------------------------------------------------------
# is_configured & ping
# ---------------------------------------------------------------------------

def test_is_configured_always_true(client):
    assert client.is_configured is True


@pytest.mark.asyncio
async def test_ping_always_true(client):
    assert await client.ping() is True


# ---------------------------------------------------------------------------
# chat – role detection by system prompt
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_optimist_response(client):
    result = await client.chat(
        system_prompt='You are Agent 1: The Expansive Optimist.',
        user_prompt='How does AI affect education?',
    )
    assert 'Optimist' in result
    assert 'AI affect education' in result
    assert 'opportunit' in result.lower()


@pytest.mark.asyncio
async def test_skeptic_response(client):
    result = await client.chat(
        system_prompt='You are Agent 2: The Defensive Skeptic.',
        user_prompt='How does AI affect education?',
    )
    assert 'Skeptic' in result
    assert 'AI affect education' in result
    assert 'risk' in result.lower()


@pytest.mark.asyncio
async def test_peer_review_response(client):
    result = await client.chat(
        system_prompt='You are the MetaVista Peer Review Agent.',
        user_prompt='test query',
    )
    assert 'Consensus' in result
    assert 'Conflicts' in result
    assert 'Critique summary' in result


@pytest.mark.asyncio
async def test_synthesis_response(client):
    result = await client.chat(
        system_prompt='You are the MetaVista Master Synthesizer.',
        user_prompt='What is the future of work?',
    )
    assert 'Verified Research Report' in result
    assert 'future of work' in result
    assert 'Executive Summary' in result
    assert 'Final Recommendation' in result


@pytest.mark.asyncio
async def test_generic_fallback(client):
    result = await client.chat(
        system_prompt='You are a helpful assistant.',
        user_prompt='Tell me about cats',
    )
    assert 'Mock response' in result
    assert 'cats' in result.lower()


# ---------------------------------------------------------------------------
# Deterministic output
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_same_input_same_output(client):
    r1 = await client.chat('You are the Expansive Optimist.', 'test query')
    r2 = await client.chat('You are the Expansive Optimist.', 'test query')
    assert r1 == r2


# ---------------------------------------------------------------------------
# Latency simulation
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_simulated_latency():
    c = MockClient(latency_ms=100)
    start = time.monotonic()
    await c.chat('You are the Optimist.', 'latency test')
    elapsed = time.monotonic() - start
    assert elapsed >= 0.09  # allow small margin


@pytest.mark.asyncio
async def test_zero_latency_is_fast(client):
    start = time.monotonic()
    await client.chat('You are the Optimist.', 'speed test')
    elapsed = time.monotonic() - start
    assert elapsed < 0.05


# ---------------------------------------------------------------------------
# Drop-in compatibility with OpenAICompatibleClient interface
# ---------------------------------------------------------------------------

def test_has_required_attributes(client):
    """MockClient exposes the same public attributes as OpenAICompatibleClient."""
    assert hasattr(client, 'chat')
    assert hasattr(client, 'ping')
    assert hasattr(client, 'is_configured')
    assert hasattr(client, 'provider_name')
    assert hasattr(client, 'api_key')
    assert hasattr(client, 'model')
    assert hasattr(client, 'base_url')


def test_custom_provider_name():
    c = MockClient(provider_name='MockQwen')
    assert c.provider_name == 'MockQwen'
