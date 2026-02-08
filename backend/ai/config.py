from pydantic_settings import BaseSettings
from typing import Optional


class AIConfig(BaseSettings):
    cohere_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields in .env that aren't defined in the model


# Global config instance
ai_config = AIConfig()