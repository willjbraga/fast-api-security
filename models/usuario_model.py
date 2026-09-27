from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

from models.artigo_model import ArtigoModel

from enum import Enum

from core.base import Base

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
    senha: Mapped[str] = mapped_column(String(512), nullable=False)
    acesso: Mapped[TipoAcessoEnum] = mapped_column(PGEnum(TipoAcessoEnum, name= "tipo_acesso_enum", values_callable=lambda enum: [item.value for item in enum],), default=TipoAcessoEnum.USER, nullable= False)
    artigos: Mapped[list['ArtigoModel']] = relationship( back_populates='criador', cascade='all, delete-orphan', lazy='raise_on_sql',)