from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class ArtigoBase(BaseModel): 
    titulo: str = Field(min_length=1, max_length=256) 
    descricao: str = Field(min_length=1, max_length=256) 
    url_fonte: HttpUrl
    
class ArtigoCreate(ArtigoBase): 
    model_config = ConfigDict(extra='forbid')
    
class ArtigoUpdate(BaseModel): 
    model_config = ConfigDict(extra='forbid') 
    titulo: str | None = Field(None, min_length=1, max_length=256) 
    descricao: str | None = Field(None, min_length=1, max_length=256) 
    url_fonte: HttpUrl | None = None
    
class ArtigoResponse(ArtigoBase): 
    model_config = ConfigDict(from_attributes=True) 
    id: int
    usuario_id: int