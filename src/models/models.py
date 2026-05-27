# Arquivo de configuracao Models

from sqlalchemy import Column, Float, Integer, String
from connection.connection import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_name = Column(String, index=True)
    cliente_email = Column(String, unique=True, index=True)
    tipo_solicitacao = Column(String)
    valor_patrimonio = Column(Float)
    status = Column(String, default="Pendente")