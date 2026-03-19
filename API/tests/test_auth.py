from jsonschema import validate

def test_login(api_client):
    payload = {
        "email": "test@test.com",
        "password": "password123",
    }
    response = api_client.post("/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json()

def test_user_schema(api_client, user_schema):
    response = api_client.get("/users/1")

    validate(instance=response.json(), schema=user_schema)