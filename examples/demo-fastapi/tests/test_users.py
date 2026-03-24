from fastapi.testclient import TestClient


def test_create_user(client: TestClient) -> None:
    response = client.post("/users/", json={"name": "Ana García", "email": "ana@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ana García"
    assert data["email"] == "ana@example.com"
    assert "id" in data


def test_create_user_duplicate_email(client: TestClient) -> None:
    payload = {"name": "Ana García", "email": "ana@example.com"}
    client.post("/users/", json=payload)
    response = client.post("/users/", json=payload)
    assert response.status_code == 409


def test_get_user(client: TestClient) -> None:
    created = client.post("/users/", json={"name": "Luis", "email": "luis@example.com"}).json()
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == "luis@example.com"


def test_get_user_not_found(client: TestClient) -> None:
    response = client.get("/users/999")
    assert response.status_code == 404


def test_list_users(client: TestClient) -> None:
    client.post("/users/", json={"name": "A", "email": "a@example.com"})
    client.post("/users/", json={"name": "B", "email": "b@example.com"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_user(client: TestClient) -> None:
    created = client.post("/users/", json={"name": "Old", "email": "old@example.com"}).json()
    response = client.put(f"/users/{created['id']}", json={"name": "New", "email": "new@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "New"


def test_delete_user(client: TestClient) -> None:
    created = client.post("/users/", json={"name": "Temp", "email": "temp@example.com"}).json()
    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/users/{created['id']}").status_code == 404
