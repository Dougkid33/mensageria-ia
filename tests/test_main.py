from fastapi.testclient import TestClient
from sms_ia.app.main import app

client = TestClient(app)

def test_ping():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "API ok"}

def test_create_contato():
    response = client.post("/contatos/", json={
        "nome": "John Doe",
        "numero_telefone": "987654321",
        "grupo": "Friends"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data  # O ID do novo contato foi retornado

def test_get_contato():
    response = client.get("/contatos/1")  # Supondo que o ID 1 existe
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "John Doe"

def test_update_contato():
    response = client.put("/contatos/1", json={
        "nome": "John Updated",
        "numero_telefone": "123456789",
        "grupo": "Family"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "John Updated"

def test_delete_contato():
    response = client.delete("/contatos/1")  # Supondo que o ID 1 existe
    assert response.status_code == 204
