
import strawberry
from strawberry.types import Info

from src.connection.connection import AsyncSessionLocal
from src.models.models import Cliente
from src.schema.types import UserType, WebhookResultType
from src.services.cliente_service import valida_dados, verifica_email
from src.services.webhook_service import processar_webhook


@strawberry.input
class ClienteInput:
    """Criando os campos que podem ser alterados na api"""
    cliente_name: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float


@strawberry.input
class WebhookInput:
    """Input para processar webhook do Pipefy"""
    event_id: str
    card_id: str
    cliente_email: str
    timestamp: str


@strawberry.type
class Mutation:
    """Mutations para criar clientes e processar webhooks"""

    @strawberry.mutation
    async def create_cliente(self, info: Info, input: ClienteInput) -> UserType:
        """Cria um novo cliente no banco de dados"""

        novo_cliente = Cliente(
            cliente_name=input.cliente_name,
            cliente_email=input.cliente_email,
            tipo_solicitacao=input.tipo_solicitacao,
            valor_patrimonio=input.valor_patrimonio
        )

        valida_dados(novo_cliente)

        email_duplicado = await verifica_email(novo_cliente.cliente_email)
        if email_duplicado:
            raise ValueError(f"O email '{novo_cliente.cliente_email}' já está cadastrado no sistema.")

        async with AsyncSessionLocal() as session:
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
                prioridade=novo_cliente.prioridade,
            )

    @strawberry.mutation
    async def processar_webhook_pipefy(self, info: Info, input: WebhookInput) -> WebhookResultType:
        """Processa webhook do Pipefy quando um card é atualizado"""
        resultado = await processar_webhook(
            event_id=input.event_id,
            card_id=input.card_id,
            cliente_email=input.cliente_email,
            timestamp=input.timestamp
        )

        return WebhookResultType(
            sucesso=resultado["sucesso"],
            mensagem=resultado["mensagem"],
            cliente_id=resultado.get("cliente_id"),
            prioridade=resultado.get("prioridade"),
            status=resultado.get("status")
        )
