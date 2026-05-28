import pytest
import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.main import app
from src.models.models import Base
from src.connection.connection import async_engine, AsyncSessionLocal

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Cria as tabelas de testes usando o mesmo engine da aplicação."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    """Cliente HTTP para requisições a API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
