"""Tests for services/base_openai.py – structured errors, retry, response parsing."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from services.base_openai import (
    LLMAuthError,
    LLMClientError,
    LLMConnectionError,
    LLMRateLimitError,
    LLMResponseParseError,
    LLMServerError,
    OpenAICompatibleClient,
    ProviderConfig,
    RetryConfig,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

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
# 1. Structured error hierarchy
# ---------------------------------------------------------------------------

def test_error_hierarchy():
    """All custom errors are subclasses of LLMClientError."""
    for cls in (LLMConnectionError, LLMAuthError, LLMRateLimitError, LLMServerError, LLMResponseParseError):
        assert issubclass(cls, LLMClientError)
        err = cls('Prov', 'msg')
        assert err.provider == 'Prov'
        assert 'Prov' in str(err)


def test_llm_client_error_status_code():
    err = LLMClientError('P', 'm', status_code=418)
    assert err.status_code == 418


def test_llm_client_error_no_status_code():
    err = LLMClientError('P', 'm')
    assert err.status_code is None


# ---------------------------------------------------------------------------
# 2. Missing API key
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_missing_api_key_raises():
    client = _make_client(api_key=None)
    with pytest.raises(LLMClientError, match='API key is missing'):
        await client.chat('sys', 'user')


# ---------------------------------------------------------------------------
# 3. Successful chat
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_successful_chat():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'choices': [{'message': {'content': 'Hello world'}}]
    }

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        result = await client.chat('sys', 'user')
    assert result == 'Hello world'


# ---------------------------------------------------------------------------
# 4. Auth error (401 / 403)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_auth_error_401():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        with pytest.raises(LLMAuthError, match='Authentication failed'):
            await client.chat('sys', 'user')


@pytest.mark.asyncio
async def test_auth_error_403():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 403

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        with pytest.raises(LLMAuthError):
            await client.chat('sys', 'user')


# ---------------------------------------------------------------------------
# 5. Rate limit → retry → eventually raise
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_rate_limit_retries_then_raises():
    retry_cfg = RetryConfig(max_retries=2, backoff_base=0.01)
    config = ProviderConfig(retry=retry_cfg)
    client = _make_client(config=config)

    mock_response = MagicMock()
    mock_response.status_code = 429

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        with pytest.raises(LLMRateLimitError):
            await client.chat('sys', 'user')
    # 1 initial + 2 retries = 3 calls
    assert instance.post.call_count == 3


# ---------------------------------------------------------------------------
# 6. Server error → retry → success on 2nd attempt
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_server_error_retries_then_succeeds():
    retry_cfg = RetryConfig(max_retries=2, backoff_base=0.01)
    config = ProviderConfig(retry=retry_cfg)
    client = _make_client(config=config)

    fail_response = MagicMock()
    fail_response.status_code = 503

    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {
        'choices': [{'message': {'content': 'Recovered'}}]
    }

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(side_effect=[fail_response, success_response])
        result = await client.chat('sys', 'user')
    assert result == 'Recovered'
    assert instance.post.call_count == 2


# ---------------------------------------------------------------------------
# 7. Connection error
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_connection_error():
    client = _make_client()

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(side_effect=httpx.ConnectError('refused'))
        with pytest.raises(LLMConnectionError, match='Connection failed'):
            await client.chat('sys', 'user')


# ---------------------------------------------------------------------------
# 8. Timeout error
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_timeout_error():
    client = _make_client()

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(side_effect=httpx.TimeoutException('read timeout'))
        with pytest.raises(LLMConnectionError, match='timed out'):
            await client.chat('sys', 'user')


# ---------------------------------------------------------------------------
# 9. Malformed response
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_malformed_response():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'error': 'no choices here'}

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        with pytest.raises(LLMResponseParseError, match='Unexpected response shape'):
            await client.chat('sys', 'user')


# ---------------------------------------------------------------------------
# 10. ProviderConfig defaults
# ---------------------------------------------------------------------------

def test_provider_config_defaults():
    cfg = ProviderConfig()
    assert cfg.connect_timeout == 10.0
    assert cfg.read_timeout == 60.0
    assert cfg.retry.max_retries == 3


def test_custom_config_passed_to_client():
    cfg = ProviderConfig(connect_timeout=5.0, read_timeout=30.0, retry=RetryConfig(max_retries=1))
    client = _make_client(config=cfg)
    assert client.config.connect_timeout == 5.0
    assert client.config.read_timeout == 30.0
    assert client.config.retry.max_retries == 1


# ---------------------------------------------------------------------------
# 11. Other 4xx error
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_generic_client_error():
    client = _make_client()
    mock_response = MagicMock()
    mock_response.status_code = 400

    with patch('httpx.AsyncClient') as MockAsyncClient:
        instance = MockAsyncClient.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=mock_response)
        with pytest.raises(LLMClientError, match='Client error'):
            await client.chat('sys', 'user')
