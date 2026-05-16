"""Tests for the three client subclasses – instantiation and per-provider config."""

import pytest

from config.settings import Settings
from services.qwen_client import QwenClient, QWEN_PROVIDER_CONFIG
from services.zai_client import ZaiClient, ZAI_PROVIDER_CONFIG
from services.tokenrouter_client import TokenRouterClient, TOKENROUTER_PROVIDER_CONFIG


# ---------------------------------------------------------------------------
# Helper – build Settings with env vars (bypasses .env file)
# ---------------------------------------------------------------------------

def _settings(**overrides) -> Settings:
    """Build Settings without reading the .env file (isolated for testing)."""
    defaults = dict(
        QWEN_API_KEY='sk-qwen-test',
        ZAI_API_KEY='sk-zai-test',
        TOKENROUTER_API_KEY='sk-tr-test',
        TOKENROUTER_BASE_URL='https://api.tokenrouter.com/v1',
    )
    defaults.update(overrides)
    # _env_file=None prevents pydantic-settings from reading .env
    return Settings(_env_file=None, **defaults)


# ---------------------------------------------------------------------------
# QwenClient
# ---------------------------------------------------------------------------

def test_qwen_client_instantiation():
    s = _settings()
    client = QwenClient(s)
    assert client.provider_name == 'Qwen Cloud'
    assert client.model == 'qwen-plus'
    assert client.api_key == 'sk-qwen-test'
    assert client.base_url == 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
    # Per-provider config
    assert client.config is QWEN_PROVIDER_CONFIG
    assert client.config.read_timeout == 90.0
    assert client.config.retry.max_retries == 3
    assert client.config.retry.backoff_base == 1.5


def test_qwen_client_custom_model():
    s = _settings(QWEN_MODEL='qwen-max')
    client = QwenClient(s)
    assert client.model == 'qwen-max'


# ---------------------------------------------------------------------------
# ZaiClient
# ---------------------------------------------------------------------------

def test_zai_client_instantiation():
    s = _settings()
    client = ZaiClient(s)
    assert client.provider_name == 'Z.ai'
    assert client.model == 'glm-4-plus'
    assert client.api_key == 'sk-zai-test'
    assert client.base_url == 'https://open.bigmodel.cn/api/paas/v4'
    assert client.config is ZAI_PROVIDER_CONFIG
    assert client.config.read_timeout == 120.0


# ---------------------------------------------------------------------------
# TokenRouterClient
# ---------------------------------------------------------------------------

def test_tokenrouter_client_instantiation():
    s = _settings()
    client = TokenRouterClient(s)
    assert client.provider_name == 'TokenRouter'
    assert client.config is TOKENROUTER_PROVIDER_CONFIG
    assert client.config.connect_timeout == 8.0
    assert client.config.retry.max_retries == 2


def test_tokenrouter_requires_base_url():
    s = _settings(TOKENROUTER_BASE_URL=None)
    with pytest.raises(RuntimeError, match='TOKENROUTER_BASE_URL'):
        TokenRouterClient(s)


# ---------------------------------------------------------------------------
# Config isolation – each client has its own config
# ---------------------------------------------------------------------------

def test_configs_are_independent():
    s = _settings()
    q = QwenClient(s)
    z = ZaiClient(s)
    t = TokenRouterClient(s)

    assert q.config is not z.config
    assert z.config is not t.config
    # Different read timeouts prove they are provider-specific
    assert q.config.read_timeout == 90.0
    assert z.config.read_timeout == 120.0
    assert t.config.read_timeout == 60.0
