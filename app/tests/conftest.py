from typing import Generator

import os
import pytest

from app.tests.test_db import sessionmaker_for_test, SQLALCHEMY_DATABASE_URL, TEST_DB_PATH
from app.tests.test_env_var import TEST_ENV_VAR


# saving the env var before overwritting them with test settings
saved_env_var = dict(os.environ)


def pytest_configure(config):  # pylint: disable=unused-argument
    # inject test env var before fastapi app is loaded
    os.environ.update(TEST_ENV_VAR)


@pytest.fixture(scope="session", autouse=True)
def setup_env_var():
    # executed before test session
    yield
    # executed after test session
    os.environ.update(saved_env_var)  # restore saved env var


@pytest.fixture(scope="session")
def db_path():
    return TEST_DB_PATH


@pytest.fixture(scope="session")
def db_uri():
    return SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope="session")
def db(db_uri, db_path) -> Generator:  # pylint: disable=redefined-outer-name
    try:
        session = sessionmaker_for_test(db_uri)()
        yield session
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)  # cleanup after test
