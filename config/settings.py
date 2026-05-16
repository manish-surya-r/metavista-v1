from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_env: str = Field(default='development', alias='APP_ENV')
    mock_mode: bool = Field(default=False, alias='MOCK_MODE')

    qwen_api_key: str | None = Field(default=None, alias='QWEN_API_KEY')
    qwen_base_url: str = Field(default='https://dashscope-intl.aliyuncs.com/compatible-mode/v1', alias='QWEN_BASE_URL')
    qwen_model: str = Field(default='qwen-plus', alias='QWEN_MODEL')

    zai_api_key: str | None = Field(default=None, alias='ZAI_API_KEY')
    zai_base_url: str = Field(default='https://open.bigmodel.cn/api/paas/v4', alias='ZAI_BASE_URL')
    zai_model: str = Field(default='glm-4-plus', alias='ZAI_MODEL')

    tokenrouter_api_key: str | None = Field(default=None, alias='TOKENROUTER_API_KEY')
    tokenrouter_base_url: str | None = Field(default=None, alias='TOKENROUTER_BASE_URL')
    tokenrouter_model: str = Field(default='qwen-plus', alias='TOKENROUTER_MODEL')
    use_tokenrouter: bool = Field(default=False, alias='USE_TOKENROUTER')

    @property
    def should_mock(self) -> bool:
        return self.mock_mode or not self.qwen_api_key

    @property
    def should_mock_final(self) -> bool:
        return self.mock_mode or not self.zai_api_key


@lru_cache
def get_settings() -> Settings:
    return Settings()
