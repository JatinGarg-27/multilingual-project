from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/tts_copilot"

    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60

    generation_service_url: str = "http://localhost:8001"
    tts_service_url: str = "http://localhost:8002"

    supported_languages: tuple[str, ...] = ("de", "fr", "es", "ta", "te", "kn")


settings = Settings()
