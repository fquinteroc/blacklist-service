import json

import pytest

valid_headers = {
    "Authorization": "Bearer secret_token_blacklist",
    "Content-Type": "application/json"
}


def test_ping(test_client):
    """Verifica que el endpoint ping retorne 'pong'."""
    response = test_client.get("/ping")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "pong"


def test_add_blacklist_missing_fields(test_client):
    """Prueba que se retorne error si faltan campos obligatorios."""
    response = test_client.post("/blacklists", headers=valid_headers, json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_add_blacklist_invalid_email(test_client):
    """Prueba que se rechace un email con formato inválido."""
    payload = {
        "email": "formato-email-incorrecto",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000"
    }
    response = test_client.post(
        "/blacklists", headers=valid_headers, json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "Formato de email inválido" in data["error"]


def test_add_blacklist_success_and_conflict(test_client):
    """Prueba la adición exitosa y luego el conflicto al intentar agregar el mismo email."""
    payload = {
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "Test de integración"
    }
    response = test_client.post(
        "/blacklists", headers=valid_headers, json=payload)
    assert response.status_code == 201
    response2 = test_client.post(
        "/blacklists", headers=valid_headers, json=payload)
    assert response2.status_code == 409


def test_get_blacklist_not_found(test_client):
    """Prueba que se retorne 404 al consultar un email inexistente."""
    response = test_client.get(
        "/blacklists/nonexistent@example.com", headers=valid_headers)
    assert response.status_code == 404


def test_get_blacklist_success(test_client):
    """Prueba la consulta exitosa de un email existente."""
    payload = {
        "email": "found@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "Razón de prueba"
    }
    test_client.post("/blacklists", headers=valid_headers, json=payload)
    response = test_client.get(
        "/blacklists/found@example.com", headers=valid_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == payload["email"]
    assert data["blocked_reason"] == payload["blocked_reason"]
