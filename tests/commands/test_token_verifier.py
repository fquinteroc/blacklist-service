import pytest
from flask import Flask, jsonify

from src.commands.token_verifier import token_required

app = Flask(__name__)


@app.route("/dummy")
@token_required
def dummy_endpoint():
    return jsonify({"msg": "Success"}), 200


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_valid_token(client):
    headers = {"Authorization": "Bearer secret_token_blacklist"}
    response = client.get("/dummy", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Success"


def test_invalid_token(client):
    headers = {"Authorization": "Bearer token_erroneo"}
    response = client.get("/dummy", headers=headers)
    assert response.status_code == 403
    data = response.get_json()
    assert "error" in data
