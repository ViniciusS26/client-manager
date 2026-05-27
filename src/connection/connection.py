import os
from unittest.mock import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

"""
Arquivo de configuração da conexão com o banco de dados usando SQLAlchemy
"""

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

async_engine = create_async_engine(DATABASE_URL, echo=True)

# Configura o construtor de sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    """Função para obter uma sessão de banco de dados, garantindo que seja fechada após o uso"""
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()