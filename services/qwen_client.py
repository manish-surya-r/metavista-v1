from config.settings import Settings
from services.base_openai import OpenAICompatibleClient, ProviderConfig, RetryConfig

# ---------------------------------------------------------------------------
# Provider metadata
# ---------------------------------------------------------------------------
# Endpoint:   https://dashscope-intl.aliyuncs.com/compatible-mode/v1
# Auth:       Bearer token (DashScope API key)
# Scopes:     chat completions
# Rate limits:
#   - qwen-plus:  ~60 RPM / 120K TPM (free tier); higher on paid plans
#   - qwen-max:  ~30 RPM / 60K TPM
#   - qwen-turbo: ~120 RPM / 240K TPM
# Docs:        https://help.aliyun.com/en/document-detail/2712195.html
# ---------------------------------------------------------------------------

QWEN_RATE_LIMITS = {
    'qwen-plus':  {'rpm': 60, 'tpm_k': 120},
    'qwen-max':   {'rpm': 30, 'tpm_k': 60},
    'qwen-turbo': {'rpm': 120, 'tpm_k': 240},
}

QWEN_PROVIDER_CONFIG = ProviderConfig(
    connect_timeout=10.0,
    read_timeout=90.0,        # qwen-plus can be slow on long prompts
    retry=RetryConfig(max_retries=3, backoff_base=1.5),
)


class QwenClient(OpenAICompatibleClient):
    """Client for Qwen Cloud (DashScope international) API."""

    def __init__(self, settings: Settings):
        super().__init__(
            api_key=settings.qwen_api_key,
            base_url=settings.qwen_base_url,
            model=settings.qwen_model,
            provider_name='Qwen Cloud',
            config=QWEN_PROVIDER_CONFIG,
        )
