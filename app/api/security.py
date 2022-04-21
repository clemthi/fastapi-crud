from typing import List

from pydantic import Json
from fastapi import Depends, HTTPException, status, Security

from app.core.security import keycloak_openid, oauth2_scheme, get_idp_public_key
from app.core.config import settings


async def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    try:
        # audience verification is disabled in case the client has 'Full Scope Allowed' set in Keycloack
        return keycloak_openid.decode_token(
            token,
            key=await get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex


async def get_current_user_roles(token_data: Json = Depends(get_auth)) -> List[str]:
    # TODO : clarify at which level the roles are managed: realm or client
    roles = token_data.get('realm_access', {}).get('roles', [])  # if role is managed at the realm level
    # roles = token_data.get('resource_access', {}).get(settings.KEYCLOACK_CLIENT_ID, {}).get('roles', [])  # if role is managed at the client level

    return roles


async def is_current_user_admin(user_roles: Json = Depends(get_current_user_roles)) -> bool:
    if settings.KEYCLOACK_ADMIN_ROLE in user_roles:
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough privilege."
    )