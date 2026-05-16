from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

import httpx

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Structured errors
# ---------------------------------------------------------------------------

class LLMClientError(Exception):
    """Base error for all LLM client failures."""
    def __init__(self, provider: str, message: str, *, status_code: int | None = None):
        self.provider = provider
        self.status_code = status_code
        super().__init__(f'[{provider}] {message}')


class LLMConnectionError(LLMClientError):
    """Network-level failure (DNS, timeout, connection refused)."""


class LLMAuthError(LLMClientError):
    """401 / 403 – invalid or expired API key."""


class LLMRateLimitError(LLMClientError):
    """429 – rate limit exceeded."""


class LLMServerError(LLMClientError):
    """5xx – upstream provider failure."""


class LLMResponseParseError(LLMClientError):
    """Unexpected response shape – missing keys, etc."""


# ---------------------------------------------------------------------------
# Retry config
# ---------------------------------------------------------------------------

@dataclass
class RetryConfig:
    max_retries: int = 3
    backoff_base: float = 1.0          # seconds; actual = backoff_base * 2 ** attempt
    retryable_statuses: tuple[int, ...] = (429, 502, 503, 504)


# ---------------------------------------------------------------------------
# Per-provider configurable settings
# ---------------------------------------------------------------------------

@dataclass
class ProviderConfig:
    connect_timeout: float = 10.0      # seconds
    read_timeout: float = 60.0         # seconds
    retry: RetryConfig = field(default_factory=RetryConfig)


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class OpenAICompatibleClient:
    def __init__(
        self,
        api_key: str | None,
        base_url: str,
        model: str,
        provider_name: str,
        config: ProviderConfig | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.provider_name = provider_name
        self.config = config or ProviderConfig()

        if not self.api_key:
            logger.warning(
                '[%s] No API key provided – calls will fail until a key is set.',
                self.provider_name,
            )

    @property
    def is_configured(self) -> bool:
        """True when an API key is present and the client is ready to make calls."""
        return bool(self.api_key)

    async def ping(self) -> bool:
        """Lightweight auth check – sends a minimal chat request.

        Returns True if the endpoint accepts the API key, False otherwise.
        Raises LLMConnectionError on network failures.
        """
        if not self.api_key:
            return False
        try:
            await self.chat(
                system_prompt='Reply with exactly: ok',
                user_prompt='ok',
                temperature=0.0,
            )
            return True
        except LLMAuthError:
            return False
        except LLMRateLimitError:
            # Rate-limited but authenticated – key is valid
            return True

    # -- public API ----------------------------------------------------------

    async def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.25) -> str:
        """Send a chat completion request with retry logic."""
        if not self.api_key:
            raise LLMClientError(self.provider_name, 'API key is missing')

        url = f'{self.base_url}/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': self.model,
            'temperature': temperature,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
        }

        last_error: Exception | None = None
        retry_cfg = self.config.retry

        for attempt in range(retry_cfg.max_retries + 1):
            try:
                timeout = httpx.Timeout(
                    connect=self.config.connect_timeout,
                    read=self.config.read_timeout,
                    write=10.0,
                    pool=10.0,
                )
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(url, headers=headers, json=payload)

                # -- structured error mapping --------------------------------
                if response.status_code == 401 or response.status_code == 403:
                    raise LLMAuthError(self.provider_name, f'Authentication failed (HTTP {response.status_code})', status_code=response.status_code)
                if response.status_code == 429:
                    raise LLMRateLimitError(self.provider_name, 'Rate limit exceeded', status_code=429)
                if response.status_code >= 500:
                    raise LLMServerError(self.provider_name, f'Upstream error (HTTP {response.status_code})', status_code=response.status_code)
                if response.status_code >= 400:
                    raise LLMClientError(self.provider_name, f'Client error (HTTP {response.status_code})', status_code=response.status_code)

                # -- parse response ------------------------------------------
                data = response.json()
                try:
                    return data['choices'][0]['message']['content']
                except (KeyError, IndexError, TypeError) as exc:
                    raise LLMResponseParseError(
                        self.provider_name,
                        f'Unexpected response shape: {exc!r} — body keys: {list(data.keys())}',
                    ) from exc

            except (LLMRateLimitError, LLMServerError) as exc:
                last_error = exc
                if attempt < retry_cfg.max_retries:
                    wait = retry_cfg.backoff_base * (2 ** attempt)
                    logger.warning(
                        '[%s] Attempt %d/%d failed (%s). Retrying in %.1fs …',
                        self.provider_name, attempt + 1, retry_cfg.max_retries + 1, exc, wait,
                    )
                    await asyncio.sleep(wait)
                    continue
                raise

            except httpx.TimeoutException as exc:
                raise LLMConnectionError(self.provider_name, f'Request timed out: {exc}') from exc

            except httpx.ConnectError as exc:
                raise LLMConnectionError(self.provider_name, f'Connection failed: {exc}') from exc

            except httpx.HTTPError as exc:
                raise LLMConnectionError(self.provider_name, f'HTTP error: {exc}') from exc

        raise last_error  # should not reach here, but safety net
