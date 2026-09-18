from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

from enum import Enum

from core.configs import Base

class TipoAcessoEnum(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class UsuarioModel(Base):
    __tablename__ = 'usuarios'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(256), nullable=False)
    sobrenome: Mapped[str | None] = mapped_column(String(256), nullable=True)
    email: Mapped[str] = mapped_column(String(256), index=True, nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(256), nullable=False)
    acesso: Mapped[TipoAcessoEnum] = mapped_column(PGEnum(TipoAcessoEnum, name= "tipo_acesso_enum", values_callable=lambda enum: [item.value for item in enum],), default=TipoAcessoEnum.USER, nullable= False)
    artigos = relationship(
        "ArtigoModel",
        cascade="all,delete-orphan",
        back_populates="criador",
        uselist=True,
        lazy="joined"
    )