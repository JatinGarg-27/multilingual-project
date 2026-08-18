from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    tts_api_base_url: str = ""
    tts_api_key: str = ""

    supported_languages: tuple[str, ...] = ("de", "fr", "es", "ta", "te", "kn")


settings = Settings()
