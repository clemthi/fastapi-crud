from app.core.config import settings
from app.tests.test_db import sessionmaker_for_test, SQLALCHEMY_DATABASE_URL


async def override_get_auth() -> dict:
    """mock jwt decripted data when logging on as user

    Returns:
        dict: mocked jwt decripted data
    """
    return {}


async def override_get_auth_admin() -> dict:
    """fake jwt decripted data when logging on as admin

    Returns:
        dict: mocked jwt decripted data
    """
    return {
        'realm_access': {'roles': [settings.KEYCLOACK_ADMIN_ROLE]},
        'resource_access': {settings.KEYCLOACK_CLIENT_ID: {'roles': [settings.KEYCLOACK_ADMIN_ROLE]}},
    }


async def override_get_db():
    try:
        session = sessionmaker_for_test(SQLALCHEMY_DATABASE_URL)()
        yield session
    finally:
        pass
