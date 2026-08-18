from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/tts_copilot"

    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60

    llm_api_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = ""

    tts_api_base_url: str = ""
    tts_api_key: str = ""

    supported_languages: tuple[str, ...] = ("de", "fr", "es", "ta", "te", "kn")


settings = Settings()
