import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.models.blacklist import Base

load_dotenv('.env.development')


class SessionConfig():
    def __init__(self):
        pass

    def url(self):
        if os.environ.get("ENV") == "testing":
            return os.environ.get("DB_URL", "sqlite:///:memory:")

        db_url = os.getenv("DB_URL")
        if db_url:
            return db_url
        db_user = os.environ['RDS_USERNAME']
        db_pass = os.environ['RDS_PASSWORD']
        db_host = os.environ['RDS_HOSTNAME']
        db_port = os.environ['RDS_PORT']
        db_name = os.environ['RDS_DB_NAME']
        return f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'


session_config = SessionConfig()
engine = create_engine(session_config.url())

Base.metadata.bind = engine
Session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)
