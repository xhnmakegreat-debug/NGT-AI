"""FastAPI 应用配置"""

from typing import List

try:
    from pydantic_settings import BaseSettings
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "缺少依赖 pydantic-settings，请先运行 `pip install pydantic-settings`。"
    ) from exc


class Settings(BaseSettings):
    """后端通用配置"""

    app_name: str = "NGT-AI Decision System"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["*"]
    use_real_apis: bool = False

    database_url: str = "postgresql+psycopg://ngtai:ngtai@localhost:5432/ngtai"
    database_echo: bool = False

    redis_url: str | None = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60 * 24

    class Config:
        env_file = ".env"

    class Config:
        env_file = ".env"


settings = Settings()
