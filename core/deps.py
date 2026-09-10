from typing import AsyncGenerator, Optional

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
    subject: Optional[str] = None

async def get_session() -> AsyncGenerator[AsyncSession, None]:
     
     session: AsyncSession = Session()

     try:
          yield session
     finally:
          await session.close()

async def get_current_user(
     db: AsyncSession = Depends(get_session),
     token: str = Depends(OAuth2_schema)) -> UsuarioModel:
     credential_exception: HTTPException = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Não foi possível autenticar a credencial",
          headers={"WWW-Authenticate": "Bearer"}
     )

     try:
          payload = jwt.decode(
               token,
               settings.JWT_SECRET,
               algorithms=[settings.ALGORITHM],
               options={"verify_aud": False}
          )
          username: str = payload.get("sub")

          if username is None:
               raise credential_exception

          token_data: TokenData = TokenData(username=username)

     except jwt.exceptions.InvalidTokenError:
          raise credential_exception

     query = select(UsuarioModel).where(
          UsuarioModel.id == int(token_data.username)
     )

     result = await db.execute(query)

     usuario: UsuarioModel | None = result.scalar_one_or_none()

     if usuario is None:
          raise credential_exception

     return usuario
