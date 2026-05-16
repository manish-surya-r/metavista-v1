from config.settings import Settings
from services.base_openai import OpenAICompatibleClient


class QwenClient(OpenAICompatibleClient):
    def __init__(self, settings: Settings):
        super().__init__(
            api_key=settings.qwen_api_key,
            base_url=settings.qwen_base_url,
            model=settings.qwen_model,
            provider_name='Qwen Cloud',
        )
