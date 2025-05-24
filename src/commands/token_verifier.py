from functools import wraps

from flask import jsonify, request

from src.errors.errors import Unauthorized


def is_token_invalid(headers):
    token = headers.get("Authorization", "")
    if not token or not token.startswith("Bearer "):
        raise Unauthorized()

    valid_token = "Bearer secret_token_blacklist"
    if token != valid_token:
        raise Unauthorized()

    return None


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            is_token_invalid(request.headers)
        except Unauthorized as e:
            return jsonify({"error": e.description}), e.code
        return f(*args, **kwargs)
    return decorated_function
