from config.settings import Settings
from services.qwen_client import QwenClient
from services.tokenrouter_client import TokenRouterClient
from services.zai_client import ZaiClient


class ModelRouter:
    """Simple routing layer.

    MVP behavior:
    - critique and peer-review agents use TokenRouter when enabled
    - otherwise they use Qwen Cloud
    - final synthesis uses Z.ai
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.qwen = QwenClient(settings)
        self.zai = ZaiClient(settings)
        self.tokenrouter = None
        if settings.use_tokenrouter:
            self.tokenrouter = TokenRouterClient(settings)

    def critique_client(self):
        return self.tokenrouter or self.qwen

    def peer_review_client(self):
        return self.tokenrouter or self.qwen

    def synthesis_client(self):
        return self.zai
