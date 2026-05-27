import strawberry
from strawberry.types import Info
from sqlalchemy.future import select

from src.connection.connection import AsyncSessionLocal
from src.models.models import Cliente
from src.graphql.types import UserType

"""
Mutation para criar um novo cliente no banco de dados, utilizando o ClienteType para estruturar a resposta
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}
"""
"""
Criando os campos que podem ser alterados na api
"""
@strawberry.input
class ClienteInput:
    cliente_name: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_cliente(self, info: Info, input: ClienteInput) -> UserType:
        """Cria um novo cliente no banco de dados e retorna os dados do cliente criado"""
        async with AsyncSessionLocal() as session:
            novo_cliente = Cliente(
                cliente_name=input.cliente_name,
                cliente_email=input.cliente_email,
                tipo_solicitacao=input.tipo_solicitacao,
                valor_patrimonio=input.valor_patrimonio
            )
            session.add(novo_cliente)
            await session.commit()
            await session.refresh(novo_cliente)
            return UserType(
                id=novo_cliente.id,
                cliente_name=novo_cliente.cliente_name,
                cliente_email=novo_cliente.cliente_email,
                status=novo_cliente.status,
            )