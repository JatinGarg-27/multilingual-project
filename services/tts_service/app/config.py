from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    elevenlabs_api_key: str = ""
    elevenlabs_base_url: str = "https://api.elevenlabs.io/v1/text-to-speech"
    elevenlabs_model_id: str = "eleven_multilingual_v2"
    # "Rachel" — ElevenLabs' standard premade voice, available on every account.
    default_voice_id: str = "21m00Tcm4TlvDq8ikWAM"

    # Used to build the audio_url returned to callers. Set to the address callers
    # can actually reach this service at (http://tts-service:8002 inside docker
    # compose, http://localhost:8002 for local non-docker dev).
    public_base_url: str = "http://localhost:8002"
    audio_storage_dir: str = "audio_output"

    # Every language this project claims to support (per the resume bullet).
    # NOTE: ElevenLabs' eleven_multilingual_v2 model does not officially list
    # Telugu or Kannada as supported languages (as of this writing) — see
    # DECISION-004 in DECISION_LOG.md. Requests for "te"/"kn" are still accepted
    # and forwarded, but audio quality/accuracy for those two is not guaranteed.
    supported_languages: tuple[str, ...] = ("de", "fr", "es", "ta", "te", "kn")
    unverified_languages: tuple[str, ...] = ("te", "kn")


settings = Settings()
