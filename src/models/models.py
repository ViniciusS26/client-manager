# Arquivo de configuracao Models

from sqlalchemy import Float, Integer, String, DateTime
from src.connection.connection import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cliente_name: Mapped[str] = mapped_column(String, index=True)
    cliente_email: Mapped[str] = mapped_column(String, unique=True, index=True)
    tipo_solicitacao: Mapped[str] = mapped_column(String)
    valor_patrimonio: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="Aguardando análise")
    prioridade: Mapped[str] = mapped_column(String, default="prioridade_normal")


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    card_id: Mapped[str] = mapped_column(String)
    cliente_email: Mapped[str] = mapped_column(String, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    processado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
