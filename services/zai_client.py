from config.settings import Settings
from services.base_openai import OpenAICompatibleClient, ProviderConfig, RetryConfig

# ---------------------------------------------------------------------------
# Provider metadata
# ---------------------------------------------------------------------------
# Endpoint:   https://open.bigmodel.cn/api/paas/v4
# Auth:       Bearer token (Zhipu API key)
# Scopes:     chat completions
# Rate limits:
#   - glm-4-plus: ~60 RPM (free tier); higher on paid plans
#   - glm-4:      ~60 RPM
#   - glm-4-flash: ~120 RPM
# Docs:        https://open.bigmodel.cn/dev/api/normal-model/glm-4
# ---------------------------------------------------------------------------

ZAI_RATE_LIMITS = {
    'glm-4-plus':  {'rpm': 60, 'tpm_k': 120},
    'glm-4':       {'rpm': 60, 'tpm_k': 120},
    'glm-4-flash': {'rpm': 120, 'tpm_k': 240},
}

ZAI_PROVIDER_CONFIG = ProviderConfig(
    connect_timeout=10.0,
    read_timeout=120.0,       # glm-4-plus synthesis can be slow
    retry=RetryConfig(max_retries=3, backoff_base=1.5),
)


class ZaiClient(OpenAICompatibleClient):
    """Client for Z.ai (Zhipu BigModel) API."""

    def __init__(self, settings: Settings):
        super().__init__(
            api_key=settings.zai_api_key,
            base_url=settings.zai_base_url,
            model=settings.zai_model,
            provider_name='Z.ai',
            config=ZAI_PROVIDER_CONFIG,
        )
