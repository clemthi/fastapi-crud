from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

# path of sqlite file mocking the db during the tests
TEST_DB_PATH = './test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite:///{TEST_DB_PATH}'


def sessionmaker_for_test(db_url: str) -> sessionmaker:
    params = {}
    # disable warning for sqlite
    if 'sqlite' in db_url:
        params['connect_args'] = {'check_same_thread': False}

    engine = create_engine(db_url, **params)
    Base.metadata.create_all(bind=engine)  # pylint: disable=no-member

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
