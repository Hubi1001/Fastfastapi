"""Automated tests of the user CRUD API (run with: pytest)."""

JAN = {"name": "Jan Kowalski", "email": "jan.kowalski@example.com", "role": "admin"}
ANNA = {"name": "Anna Nowak", "email": "anna.nowak@example.com", "role": "user"}


def create(client, data):
    response = client.post("/users/", json=data)
    assert response.status_code == 201, response.text
    return response.json()


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_and_get_user(client):
    user = create(client, JAN)
    assert user == {**JAN, "id": user["id"]}
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json() == user


def test_list_users(client):
    a, b = create(client, JAN), create(client, ANNA)
    response = client.get("/users/")
    assert response.status_code == 200
    assert [u["id"] for u in response.json()] == [a["id"], b["id"]]


def test_duplicate_email_is_rejected(client):
    create(client, JAN)
    response = client.post("/users/", json={**JAN, "name": "Someone Else"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_invalid_payloads_are_rejected(client):
    assert client.post("/users/", json={**JAN, "email": "not-an-email"}).status_code == 422
    assert client.post("/users/", json={**JAN, "name": ""}).status_code == 422
    assert client.post("/users/", json={"name": "Only Name"}).status_code == 422
    assert client.post("/users/", json={**JAN, "role": "x" * 101}).status_code == 422


def test_partial_update_changes_only_sent_fields(client):
    user = create(client, JAN)
    response = client.put(f"/users/{user['id']}", json={"role": "moderator"})
    assert response.status_code == 200
    assert response.json() == {**user, "role": "moderator"}


def test_null_in_update_leaves_field_unchanged(client):
    user = create(client, JAN)
    response = client.put(f"/users/{user['id']}", json={"name": None})
    assert response.status_code == 200
    assert response.json()["name"] == JAN["name"]


def test_update_to_taken_email_is_rejected(client):
    create(client, JAN)
    anna = create(client, ANNA)
    response = client.put(f"/users/{anna['id']}", json={"email": JAN["email"]})
    assert response.status_code == 400


def test_update_with_invalid_email_is_rejected(client):
    user = create(client, JAN)
    assert client.put(f"/users/{user['id']}", json={"email": "bad"}).status_code == 422


def test_missing_user_returns_404(client):
    assert client.get("/users/999").status_code == 404
    assert client.put("/users/999", json={"name": "X"}).status_code == 404
    assert client.delete("/users/999").status_code == 404


def test_non_numeric_id_returns_422(client):
    assert client.get("/users/abc").status_code == 422


def test_delete_user(client):
    user = create(client, JAN)
    assert client.delete(f"/users/{user['id']}").status_code == 200
    assert client.get(f"/users/{user['id']}").status_code == 404


def test_cors_allows_only_configured_origin(client):
    allowed = client.options(
        "/users/", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"}
    )
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:5173"
    blocked = client.get("/users/", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in blocked.headers
