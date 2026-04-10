from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "TechDoc AI API"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    valid_api_keys: str = "sk-dev-key-123456789"
    ai_backend: str = "stub"
    cohere_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    rate_limit: str = "10/minute"

    @property
    def api_keys_list(self) -> List[str]:
        return [k.strip() for k in self.valid_api_keys.split(",") if k.strip()]


settings = Settings()