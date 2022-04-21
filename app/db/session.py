from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def get_engine(db_uri: str):
    params = {
        'pool_pre_ping': True,
        'echo': False,
        'future': True,
    }
    # disable warning for sqlite
    if 'sqlite' in db_uri:
        params['connect_args'] = {"check_same_thread": False}

    created_engine = create_engine(db_uri, **params)

    return created_engine


engine = get_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
