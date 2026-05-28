
import strawberry
from strawberry.types import Info
from sqlalchemy.future import select

from src.connection.connection import AsyncSessionLocal
from src.models.models import Cliente
from src.graphql.types import UserType
from src.services.cliente_service import valida_dados



@strawberry.input
class ClienteInput:
    """
        Criando os campos que podem ser alterados na api
    """
    cliente_name: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float

@strawberry.type
class Mutation:
    """
        Mutation para criar um novo cliente no banco de dados, utilizando o ClienteType para estruturar a resposta
    """


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
             
            if valida_dados(novo_cliente):
                session.add(novo_cliente)

                await session.commit()
                await session.refresh(novo_cliente)

                return UserType(
                    id=novo_cliente.id,
                    cliente_name=novo_cliente.cliente_name,
                    cliente_email=novo_cliente.cliente_email,
                    tipo_solicitacao=novo_cliente.tipo_solicitacao,
                    valor_patrimonio=novo_cliente.valor_patrimonio,
                    status=novo_cliente.status,
                )
            else:
                raise ValueError("Dados inválidos, não foi possível criar o cliente.")