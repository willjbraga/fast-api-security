from typing import Optional
from datetime import datetime, timedelta, timezone

from models.usuario_model import TipoAcessoEnum

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha

from pydantic import EmailStr

OAuth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> UsuarioModel | None:
    result = await db.execute(
        select(UsuarioModel).where(
            UsuarioModel.email == email
        )
    )
    
    usuario: UsuarioModel = result.scalar_one_or_none()

    if usuario is None:
        return None

    if not verificar_senha(senha, usuario.senha):
        return None

    return usuario

def _normalizar_role(role: TipoAcessoEnum | str) -> str:
    if isinstance(role, TipoAcessoEnum):
        return role.value

    return role

def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str, role: str) -> str:

    agora = datetime.now(timezone.utc)

    payload = {
        "type" : tipo_token,
        "sub" : str(sub),
        "role": _normalizar_role(role),
        "iat" : agora,
        "exp" : agora + tempo_vida
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str, role: str) -> str:

    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
        role=role
    )