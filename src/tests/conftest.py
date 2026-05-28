import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.main import app
from src.models.models import Base
from src.connection.connection import AsyncSessionLocal

""" Banco em memória SQLite separado para testes"""
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Cria as tabelas de testes."""
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    """Cliente HTTP  para  requisições a API."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac