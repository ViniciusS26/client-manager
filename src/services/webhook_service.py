from datetime import datetime, timezone
from sqlalchemy.future import select
from src.connection.connection import AsyncSessionLocal
from src.models.models import Cliente, WebhookEvent


def _parse_timestamp(timestamp: str) -> datetime:
    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


async def processar_webhook(event_id: str, card_id: str, cliente_email: str, timestamp: str) -> dict:
    """
    Processa webhook do Pipefy para atualizar cliente com prioridade.

    Regras:
    - Verifica idempotência pelo event_id
    - Busca cliente pelo cliente_email
    - Define prioridade baseado em valor_patrimonio:
      * >= 200.000: prioridade_alta
      * < 200.000: prioridade_normal
    - Atualiza status para "Processado"
    """
    async with AsyncSessionLocal() as session:
        # 1. Verificar idempotência
        result = await session.execute(
            select(WebhookEvent).where(WebhookEvent.event_id == event_id)
        )
        evento_existente = result.scalars().first()

        if evento_existente:
            return {
                "sucesso": False,
                "mensagem": f"Evento {event_id} já foi processado anteriormente.",
                "duplicado": True
            }

        # 2. Buscar cliente pelo email
        result = await session.execute(
            select(Cliente).where(Cliente.cliente_email == cliente_email)
        )
        cliente = result.scalars().first()

        if not cliente:
            return {
                "sucesso": False,
                "mensagem": f"Cliente com email {cliente_email} não encontrado.",
                "cliente_encontrado": False
            }

        # 3. Definir prioridade baseado em valor_patrimonio
        prioridade = "prioridade_alta" if cliente.valor_patrimonio >= 200000 else "prioridade_normal"

        # 4. Atualizar cliente
        cliente.status = "Processado"
        cliente.prioridade = prioridade

        # 5. Registrar webhook como processado
        webhook_event = WebhookEvent(
            event_id=event_id,
            card_id=card_id,
            cliente_email=cliente_email,
            timestamp=_parse_timestamp(timestamp)
        )

        session.add(webhook_event)
        await session.commit()

        return {
            "sucesso": True,
            "mensagem": f"Webhook processado com sucesso para cliente {cliente_email}",
            "cliente_id": cliente.id,
            "prioridade": prioridade,
            "status": cliente.status
        }


def gerar_mutation_pipefy_update_card(card_id: str, prioridade: str) -> str:
    """
    Gera a mutation GraphQL do Pipefy para atualizar um card com a prioridade calculada.

    Documentação: https://developers.pipefy.com/reference/graphql-api
    """
    prioridade_pipefy = "red" if prioridade == "prioridade_alta" else "yellow"

    mutation = f"""
    mutation {{
      updateCardField(input: {{
        cardId: "{card_id}"
        fieldId: "priority_field"
        value: "{prioridade_pipefy}"
      }}) {{
        card {{
          id
          title
          status {{
            name
          }}
        }}
      }}
    }}
    """

    return mutation.strip()
