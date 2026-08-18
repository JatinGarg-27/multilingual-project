import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.db.base import Base
from app.main import app
from app.services import tts_client as tts_client_module
from app.services.generation_client import generation_client
from app.services.tts_client import UnsupportedLanguageError

engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SUPPORTED_LANGUAGES = {"de", "fr", "es", "ta", "te", "kn"}


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def fake_peer_services(monkeypatch):
    """content-service talks to generation-service/tts-service over HTTP in production.
    In unit tests, fake those two peers so tests don't need them running."""

    def fake_generate_draft(prompt: str) -> dict:
        return {"output": f"[fake generation] {prompt}", "model": "fake-model"}

    def fake_refine(content: str, instructions: str) -> dict:
        return {"output": f"[fake refine: {instructions}] {content}", "model": "fake-model"}

    def fake_default_voice_for(language: str) -> str:
        if language not in SUPPORTED_LANGUAGES:
            raise UnsupportedLanguageError(f"Unsupported language: {language}")
        return f"default-{language}"

    def fake_synthesize(text: str, language: str, voice_id: str) -> str:
        if language not in SUPPORTED_LANGUAGES:
            raise UnsupportedLanguageError(f"Unsupported language: {language}")
        return "stub://audio/fake.mp3"

    monkeypatch.setattr(generation_client, "generate_draft", fake_generate_draft)
    monkeypatch.setattr(generation_client, "refine", fake_refine)
    monkeypatch.setattr(tts_client_module.tts_client, "default_voice_for", fake_default_voice_for)
    monkeypatch.setattr(tts_client_module.tts_client, "synthesize", fake_synthesize)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
