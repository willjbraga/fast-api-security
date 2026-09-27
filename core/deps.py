from typing import AsyncGenerator, AsyncSessionLocal

from fastapi import Depends, HTTPException, status
import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from core.database import Session
from core.auth import OAuth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel

class TokenData(BaseModel):
    user_id: int

async def get_session() -> AsyncGenerator[AsyncSession, None]:
     async with AsyncSessionLocal() as session: 
          yield session

async def get_current_user(
     db: AsyncSession = Depends(get_session),
     token: str = Depends(OAuth2_schema)
) -> UsuarioModel:
     credential_exception: HTTPException = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Credenciais inválidas ou expiradas",
          headers={"WWW-Authenticate": "Bearer"}
     )

     try:
          payload = jwt.decode(
               token,
               settings.JWT_SECRET,
               algorithms=[settings.ALGORITHM],
               options={
                    'verify_aud': False,
                    'require': ['exp', 'iat', 'sub', 'type'],
               },
          )
          
          if payload.get('type') != 'access_token': 
               raise credential_exception
          
          user_id: str = payload.get("sub")

     except (jwt.exceptions.InvalidTokenError, ValueError, TypeError, KeyError):
          raise credential_exception from None

     result = await db.execute(
          select(UsuarioModel).where(UsuarioModel.id == user_id
     ))
     

     usuario: UsuarioModel | None = result.scalar_one_or_none()

     if usuario is None:
          raise credential_exception

     return usuario
