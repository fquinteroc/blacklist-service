import pytest

from src.errors.errors import ApiError, EmailNotFound, Unauthorized


def test_unauthorized_error():
    error = Unauthorized()
    assert error.code == 403
    assert str(error) == "Token no válido"


def test_email_not_found_error():
    error = EmailNotFound()
    assert error.code == 404
    assert str(error) == "Correo no encontrado"


def test_api_error_default():
    error = ApiError()
    assert error.code == 422
    assert str(error) == "Error"
