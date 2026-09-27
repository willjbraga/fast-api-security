from pydantic import BaseModel, ConfigDict, EmailStr, Field
from models.usuario_model import TipoAcessoEnum

class UsuarioCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1, max_length=256)
    sobrenome: str | None = Field(None, max_length=256)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)

class UsuarioUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str | None = Field(None, min_length=1, max_length=256)
    sobrenome: str | None = Field(None, max_length=256)
    email: EmailStr | None = None

class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    sobrenome: str | None
    email: EmailStr
    acesso: TipoAcessoEnum