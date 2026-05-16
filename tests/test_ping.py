"""Tests for the ping() auth check method."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from services.base_openai import (
    LLMAuthError,
    LLMClientError,
    LLMConnectionError,
    LLMRateLimitError,
    OpenAICompatibleClient,
)


def _make_client(**overrides) -> OpenAICompatibleClient:
    defaults = dict(
        api_key='test-key',
        base_url='https://api.example.com/v1',
        model='test-model',
        provider_name='TestProvider',
    )
    defaults.update(overrides)
    return OpenAICompatibleClient(**defaults)


# ---------------------------------------------------------------------------
# ping returns True on successful response
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ping_success():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'choices': [{'message': {'content': 'ok'}}]
    }

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        assert await client.ping() is True


# ---------------------------------------------------------------------------
# ping returns False on missing key
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ping_no_key():
    client = _make_client(api_key=None)
    assert await client.ping() is False


# ---------------------------------------------------------------------------
# ping returns False on auth error
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ping_auth_error():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        assert await client.ping() is False


# ---------------------------------------------------------------------------
# ping returns True on rate limit (authenticated but throttled)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ping_rate_limit_means_authenticated():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 429

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        # Rate limit means key is valid
        assert await client.ping() is True


# ---------------------------------------------------------------------------
# ping raises on connection error (not auth related)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ping_raises_on_connection_error():
    client = _make_client()

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(side_effect=httpx.ConnectError('refused'))
        with pytest.raises(LLMConnectionError):
            await client.ping()
