def _register_and_login(client, email="user@example.com", password="secret123"):
    client.post("/api/v1/auth/register", json={"email": email, "password": password})
    response = client.post("/api/v1/auth/token", data={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login(client):
    headers = _register_and_login(client)
    assert "Authorization" in headers


def test_create_and_get_content(client):
    headers = _register_and_login(client)

    create_response = client.post(
        "/api/v1/content", json={"title": "My draft", "body": "hello"}, headers=headers
    )
    assert create_response.status_code == 201
    content_id = create_response.json()["id"]

    get_response = client.get(f"/api/v1/content/{content_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "My draft"


def test_generate_persists_history(client):
    headers = _register_and_login(client)
    content_id = client.post(
        "/api/v1/content", json={"title": "Draft", "body": ""}, headers=headers
    ).json()["id"]

    response = client.post(
        f"/api/v1/content/{content_id}/generate", json={"prompt": "Write a greeting"}, headers=headers
    )
    assert response.status_code == 201
    assert response.json()["version"] == 1

    history = client.get(f"/api/v1/content/{content_id}/history", headers=headers)
    assert len(history.json()) == 1


def test_speech_rejects_unsupported_language(client):
    headers = _register_and_login(client)
    content_id = client.post(
        "/api/v1/content", json={"title": "Draft", "body": "hola"}, headers=headers
    ).json()["id"]

    response = client.post(
        f"/api/v1/content/{content_id}/speech", json={"language": "xx"}, headers=headers
    )
    assert response.status_code == 400


def test_speech_generates_stub_audio(client):
    headers = _register_and_login(client)
    content_id = client.post(
        "/api/v1/content", json={"title": "Draft", "body": "hola"}, headers=headers
    ).json()["id"]

    response = client.post(
        f"/api/v1/content/{content_id}/speech", json={"language": "es"}, headers=headers
    )
    assert response.status_code == 201
    assert response.json()["audio_url"].startswith("stub://")
