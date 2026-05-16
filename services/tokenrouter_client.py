from config.settings import Settings
from services.base_openai import OpenAICompatibleClient


class TokenRouterClient(OpenAICompatibleClient):
    def __init__(self, settings: Settings):
        if not settings.tokenrouter_base_url:
            raise RuntimeError('TOKENROUTER_BASE_URL is required when USE_TOKENROUTER=true')
        super().__init__(
            api_key=settings.tokenrouter_api_key,
            base_url=settings.tokenrouter_base_url,
            model=settings.tokenrouter_model,
            provider_name='TokenRouter',
        )
