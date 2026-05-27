
import strawberry
from typing import List
from strawberry.types import Info
from sqlalchemy import select
from src.graphql.schema import Cliente
from src.graphql.types import UserType

#querys para consultar os dados do banco de dados, utilizando o UserType para estruturar a resposta
from src.models.models import Cliente 
from src.connection.connection import AsyncSessionLocal
from src.graphql.types import UserType


@strawberry.type
class Query:

    @strawberry.field
    async def get_clientes(self, info: Info) -> List[UserType]:
        """Consulta todos os clientes cadastrados no banco de dados e retorna uma lista de UserType"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Cliente))
            clientes = result.scalars().all()
            return [UserType(
                id=cliente.id,
                cliente_name=cliente.cliente_name,
                cliente_email=cliente.cliente_email,
                tipo_solicitacao=cliente.tipo_solicitacao,
                valor_patrimonio=cliente.valor_patrimonio,
                status=cliente.status
            ) for cliente in clientes]