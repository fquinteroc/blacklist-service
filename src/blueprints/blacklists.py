import re

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from src.commands.token_verifier import token_required
from src.models.blacklist import Blacklist
from src.session import Session

blacklist_blueprint = Blueprint(
    "blacklist", __name__, url_prefix="/blacklists")


@blacklist_blueprint.route("", methods=["POST"])
@token_required
def add_to_blacklist():
    data = request.get_json()
    required_fields = ["email", "app_uuid"]

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios: email, app_uuid"}), 400

    email = data["email"]
    app_uuid = data["app_uuid"]
    blocked_reason = data.get("blocked_reason", None)

    # Validar email
    email_regex = r'^\S+@\S+\.\S+$'
    if not re.match(email_regex, email):
        return jsonify({"error": "Formato de email inválido"}), 400

    # Validar longitud del campo blocked_reason
    if blocked_reason and len(blocked_reason) > 255:
        return jsonify({"error": "El campo blocked_reason no debe exceder 255 caracteres"}), 400

    # Extraer la IP
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

    session = Session()
    try:
        blacklist_entry = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip=ip_address
        )
        session.add(blacklist_entry)
        session.commit()
        return jsonify({"msg": "Email agregado a la blacklist"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "El email ya está en la blacklist"}), 409
    finally:
        session.close()


@blacklist_blueprint.route("/<email>", methods=["GET"])
@token_required
def check_blacklist(email):
    session = Session()
    try:
        entry = session.query(Blacklist).filter_by(email=email).first()
        if entry:
            return jsonify({
                "email": entry.email,
                "app_uuid": entry.app_uuid,
                "blocked_reason": entry.blocked_reason,
                "ip": entry.ip,
                "created_at": entry.created_at.isoformat()
            }), 200
        else:
            return jsonify({"msg": "Email no está en la blacklist"}), 404
    finally:
        session.close()
