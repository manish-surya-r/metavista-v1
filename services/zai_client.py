from config.settings import Settings
from services.base_openai import OpenAICompatibleClient


class ZaiClient(OpenAICompatibleClient):
    def __init__(self, settings: Settings):
        super().__init__(
            api_key=settings.zai_api_key,
            base_url=settings.zai_base_url,
            model=settings.zai_model,
            provider_name='Z.ai',
        )
