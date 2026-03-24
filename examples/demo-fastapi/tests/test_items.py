from fastapi.testclient import TestClient


def _create_user(client: TestClient, email: str = "owner@example.com") -> int:
    return client.post("/users/", json={"name": "Owner", "email": email}).json()["id"]


def test_create_item(client: TestClient) -> None:
    owner_id = _create_user(client)
    response = client.post("/items/", json={"title": "Laptop", "description": "Dev machine", "owner_id": owner_id})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Laptop"
    assert data["owner_id"] == owner_id


def test_create_item_invalid_owner(client: TestClient) -> None:
    response = client.post("/items/", json={"title": "Ghost", "description": "", "owner_id": 999})
    assert response.status_code == 404


def test_get_item(client: TestClient) -> None:
    owner_id = _create_user(client)
    created = client.post("/items/", json={"title": "Mouse", "description": "", "owner_id": owner_id}).json()
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Mouse"


def test_get_item_not_found(client: TestClient) -> None:
    response = client.get("/items/999")
    assert response.status_code == 404


def test_list_items(client: TestClient) -> None:
    owner_id = _create_user(client)
    client.post("/items/", json={"title": "A", "description": "", "owner_id": owner_id})
    client.post("/items/", json={"title": "B", "description": "", "owner_id": owner_id})
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_item(client: TestClient) -> None:
    owner_id = _create_user(client)
    created = client.post("/items/", json={"title": "Old", "description": "", "owner_id": owner_id}).json()
    response = client.put(f"/items/{created['id']}", json={"title": "New", "description": "Updated", "owner_id": owner_id})
    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_delete_item(client: TestClient) -> None:
    owner_id = _create_user(client)
    created = client.post("/items/", json={"title": "Temp", "description": "", "owner_id": owner_id}).json()
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/items/{created['id']}").status_code == 404
