from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

from app.core.config import settings


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.KEYCLOACK_URL,
    tokenUrl=settings.KEYCLOACK_TOKEN_URL
)


keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOACK_URL,
    client_id=settings.KEYCLOACK_CLIENT_ID,
    realm_name=settings.KEYCLOACK_REALM,
    verify=True
)


async def get_idp_public_key() -> str:
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )
