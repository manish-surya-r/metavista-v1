"""Tests for API key validation at init time."""

import logging

import pytest

from services.base_openai import OpenAICompatibleClient


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
# is_configured property
# ---------------------------------------------------------------------------

def test_is_configured_true_with_key():
    client = _make_client(api_key='sk-valid')
    assert client.is_configured is True


def test_is_configured_false_without_key():
    client = _make_client(api_key=None)
    assert client.is_configured is False


def test_is_configured_false_with_empty_key():
    client = _make_client(api_key='')
    assert client.is_configured is False


# ---------------------------------------------------------------------------
# Warning emitted at init when key is missing
# ---------------------------------------------------------------------------

def test_warning_on_missing_key(caplog):
    with caplog.at_level(logging.WARNING, logger='services.base_openai'):
        _make_client(api_key=None)
    assert any('No API key provided' in r.message for r in caplog.records)


def test_no_warning_when_key_present(caplog):
    with caplog.at_level(logging.WARNING, logger='services.base_openai'):
        _make_client(api_key='sk-valid')
    assert not any('No API key provided' in r.message for r in caplog.records)
