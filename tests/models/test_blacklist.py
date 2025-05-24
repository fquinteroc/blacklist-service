import uuid
from datetime import datetime

from src.models.blacklist import Blacklist
from src.session import Session


def test_blacklist_model_creation():
    email = "model@example.com"
    app_uuid = str(uuid.uuid4())
    blocked_reason = "Prueba modelo"
    ip = "127.0.0.1"

    entry = Blacklist(email=email, app_uuid=app_uuid,
                      blocked_reason=blocked_reason, ip=ip)

    session = Session()
    session.add(entry)
    session.flush()
    session.refresh(entry)

    assert entry.email == email
    assert entry.app_uuid == app_uuid
    assert entry.blocked_reason == blocked_reason
    assert entry.ip == ip
    assert entry.created_at is not None
    assert isinstance(entry.created_at, datetime)

    session.rollback()
