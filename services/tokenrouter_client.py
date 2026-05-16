from config.settings import Settings
from services.base_openai import OpenAICompatibleClient, ProviderConfig, RetryConfig

# ---------------------------------------------------------------------------
# Provider metadata
# ---------------------------------------------------------------------------
# Endpoint:   configurable (set TOKENROUTER_BASE_URL)
# Auth:       Bearer token (TokenRouter API key)
# Scopes:     chat completions (proxied to upstream)
# Rate limits: depends on upstream provider routed to
# Docs:        https://tokenrouter.com/docs
# ---------------------------------------------------------------------------

TOKENROUTER_RATE_LIMITS: dict = {}  # passthrough – limits depend on upstream

TOKENROUTER_PROVIDER_CONFIG = ProviderConfig(
    connect_timeout=8.0,
    read_timeout=60.0,
    retry=RetryConfig(max_retries=2, backoff_base=1.0),
)


class TokenRouterClient(OpenAICompatibleClient):
    """Client for TokenRouter gateway – routes to configured upstream model."""

    def __init__(self, settings: Settings):
        if not settings.tokenrouter_base_url:
            raise RuntimeError('TOKENROUTER_BASE_URL is required when USE_TOKENROUTER=true')
        super().__init__(
            api_key=settings.tokenrouter_api_key,
            base_url=settings.tokenrouter_base_url,
            model=settings.tokenrouter_model,
            provider_name='TokenRouter',
            config=TOKENROUTER_PROVIDER_CONFIG,
        )
