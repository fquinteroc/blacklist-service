import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Blacklist(Base):
    __tablename__ = "blacklists"

    id = Column(String(36), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False, unique=True)
    app_uuid = Column(String(100), nullable=False)
    blocked_reason = Column(String(255))
    ip = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
