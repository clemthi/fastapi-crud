from typing import Any, Dict, Optional, List

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


# SQLalchemy connection string for debug database
SQLITE_PATH = 'sqlite:///db.sqlite3'


class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'
    ALLOWED_ORIGINS: List[AnyHttpUrl] = []

    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    USE_SQLITE: bool = False  # SQLite for local dev

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    CREATE_DATASET: bool = False

    KEYCLOACK_URL: str  # https://sso.example.com/auth/
    KEYCLOACK_REALM: str
    KEYCLOACK_CLIENT_ID: str
    KEYCLOACK_ADMIN_ROLE: str
    KEYCLOACK_TOKEN_URL: Optional[str] = None

    @validator('KEYCLOACK_TOKEN_URL', pre=True)
    def assemble_token_url(cls, v: Optional[str], values: Dict[str, Any]) -> Any:  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, str):
            return v

        return f"{values.get('KEYCLOACK_URL')}realms/{values.get('KEYCLOACK_REALM')}/protocol/openid-connect/token"

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, str):
            return v

        if values.get('USE_SQLITE'):
            return SQLITE_PATH

        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:    # pylint: disable=too-few-public-methods
        case_sensitive = True


settings = Settings()
