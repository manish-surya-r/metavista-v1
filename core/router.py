from config.settings import Settings
from services.mock_client import MockClient
from services.qwen_client import QwenClient
from services.tokenrouter_client import TokenRouterClient
from services.zai_client import ZaiClient


class ModelRouter:
    """Routing layer with automatic mock fallback.

    Behavior:
    - critique and peer-review agents use TokenRouter when enabled
    - otherwise they use Qwen Cloud
    - final synthesis uses Z.ai
    - any client without a configured API key falls back to MockClient
    - exposes a default_client() for the new agents/ orchestrator
    """

    def __init__(self, settings: Settings | None = None):
        from config.settings import get_settings
        self.settings = settings or get_settings()
        self.mock = MockClient()

        qwen = QwenClient(self.settings)
        self.qwen = qwen if qwen.is_configured else self.mock

        zai = ZaiClient(self.settings)
        self.zai = zai if zai.is_configured else self.mock

        self.tokenrouter = None
        if self.settings.use_tokenrouter:
            tr = TokenRouterClient(self.settings)
            self.tokenrouter = tr if tr.is_configured else self.mock

    def critique_client(self):
        return self.tokenrouter or self.qwen

    def peer_review_client(self):
        return self.tokenrouter or self.qwen

    def synthesis_client(self):
        return self.zai

    def default_client(self):
        """Return the best available client for general-purpose agent calls.

        Prefers TokenRouter > Qwen > Mock.
        """
        return self.tokenrouter or self.qwen

    @property
    def is_mock(self) -> bool:
        """True if all routes fall back to mock (no real API keys)."""
        return isinstance(self.qwen, MockClient) and isinstance(self.zai, MockClient)
