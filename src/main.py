import strawberry
from contextlib import asynccontextmanager
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.models.models import Base
from src.schema.mutations import Mutation
from src.schema.queries import Query
from src.connection.connection import async_engine
from src.routes.webhooks import router as webhooks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa quando a API liga: Cria as tabelas se elas não existirem
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI(title="Minha API", lifespan=lifespan)
app.include_router(graphql_app, prefix="/cliente")
app.include_router(webhooks_router)