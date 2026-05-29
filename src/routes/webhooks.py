from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.webhook_service import processar_webhook

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


class WebhookPayload(BaseModel):
    event_id: str
    card_id: str
    cliente_email: str
    timestamp: str


@router.post("/pipefy/card-updated")
async def webhook_card_updated(payload: WebhookPayload):
    """
    Endpoint que recebe webhook do Pipefy quando um card é atualizado.

    Processa a atualização verificando idempotência, buscando o cliente,
    definindo prioridade e atualizando o banco de dados.
    """
    resultado = await processar_webhook(
        event_id=payload.event_id,
        card_id=payload.card_id,
        cliente_email=payload.cliente_email,
        timestamp=payload.timestamp
    )

    if not resultado["sucesso"]:
        status_code = 409 if resultado.get("duplicado") else 404
        raise HTTPException(status_code=status_code, detail=resultado["mensagem"])

    return resultado
