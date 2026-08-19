from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # gTTS (Google Translate TTS) is free and needs no API key — it's used
    # for every request. See DECISION-007 in DECISION_LOG.md for why.
    public_base_url: str = "http://localhost:8002"
    audio_storage_dir: str = "audio_output"

    # gTTS genuinely supports all six of these — unlike ElevenLabs, which
    # doesn't officially support Telugu or Kannada (see DECISION-004).
    supported_languages: tuple[str, ...] = ("de", "fr", "es", "ta", "te", "kn")


settings = Settings()
