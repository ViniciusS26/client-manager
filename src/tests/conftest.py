import pytest
import os
import pytest_asyncio


os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.main import app
from src.models.models import Base
from src.connection.connection import async_engine, AsyncSessionLocal,get_db_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
 
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


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
async def client(setup_database):
    """Cliente HTTP com sessão de teste injetada via dependency override."""
 
    async def override_get_session():
        async with TestSessionLocal() as session:
            yield session
 
    # Substitui get_session em TODA a aplicação (GraphQL + REST) pelo engine de teste
    app.dependency_overrides[get_db_session] = override_get_session
 
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
 
    app.dependency_overrides.clear()
