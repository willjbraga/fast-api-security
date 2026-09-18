from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.orm import Mapped, mapped_column

from core.configs import Base

class ArtigoModel(Base):
    __tablename__ = 'artigos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(256), nullable=False)
    descricao: Mapped[str] = mapped_column(String(256), nullable=False)
    url_fonte: Mapped[str] = mapped_column(String(256), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuarios.id'), nullable=False)
    criador = relationship("UsuarioModel", back_populates='artigos', lazy='joined')