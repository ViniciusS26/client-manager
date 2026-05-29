import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_webhook_primeiro_processamento(client):
    """Cenário 1: Primeiro processamento de webhook deve ter sucesso."""
    mutation = """
        mutation {
          createCliente(input: {
            clienteName: "Cliente Webhook Test"
            clienteEmail: "webhook123@example.com"
            tipoSolicitacao: "Webhook Test"
            valorPatrimonio: 250000.00
          }) {
            id
            clienteName
            prioridade
          }
        }
    """
    response = await client.post("/cliente", json={"query": mutation})
    assert response.status_code == 200
    dados = response.json()
    assert "errors" not in dados
    assert dados["data"]["createCliente"]["prioridade"] == "prioridade_normal"

    webhook_mutation = """
        mutation {
          processarWebhookPipefy(input: {
            eventId: "evt_001"
            cardId: "card_001"
            clienteEmail: "webhook123@example.com"
            timestamp: "2026-05-28T12:00:00Z"
          }) {
            sucesso
            mensagem
            clienteId
            prioridade
            status
          }
        }
    """
    response = await client.post("/cliente", json={"query": webhook_mutation})
    assert response.status_code == 200
    dados = response.json()
    assert "errors" not in dados
    assert dados["data"]["processarWebhookPipefy"]["sucesso"] is True
    assert dados["data"]["processarWebhookPipefy"]["prioridade"] == "prioridade_alta"
    assert dados["data"]["processarWebhookPipefy"]["status"] == "Processado"


@pytest.mark.asyncio
async def test_webhook_idempotencia(client):
    """Cenário 2: Webhook duplicado deve retornar erro de duplicidade."""
    mutation = """
        mutation {
          createCliente(input: {
            clienteName: "Cliente Idempotencia"
            clienteEmail: "idempotencia456@example.com"
            tipoSolicitacao: "Test"
            valorPatrimonio: 150000.00
          }) {
            id
          }
        }
    """
    await client.post("/cliente", json={"query": mutation})

    webhook_mutation = """
        mutation {
          processarWebhookPipefy(input: {
            eventId: "evt_002"
            cardId: "card_002"
            clienteEmail: "idempotencia456@example.com"
            timestamp: "2026-05-28T12:00:00Z"
          }) {
            sucesso
            mensagem
          }
        }
    """
    response1 = await client.post("/cliente", json={"query": webhook_mutation})
    dados1 = response1.json()
    assert dados1["data"]["processarWebhookPipefy"]["sucesso"] is True

    response2 = await client.post("/cliente", json={"query": webhook_mutation})
    dados2 = response2.json()
    assert dados2["data"]["processarWebhookPipefy"]["sucesso"] is False
    assert "duplicado" in dados2["data"]["processarWebhookPipefy"]["mensagem"].lower() or \
           "já foi processado" in dados2["data"]["processarWebhookPipefy"]["mensagem"].lower()


@pytest.mark.asyncio
async def test_webhook_cliente_nao_encontrado(client):
    """Cenário 3: Webhook para cliente inexistente deve retornar erro."""
    webhook_mutation = """
        mutation {
          processarWebhookPipefy(input: {
            eventId: "evt_003"
            cardId: "card_003"
            clienteEmail: "inexistente789@example.com"
            timestamp: "2026-05-28T12:00:00Z"
          }) {
            sucesso
            mensagem
          }
        }
    """
    response = await client.post("/cliente", json={"query": webhook_mutation})
    dados = response.json()
    assert dados["data"]["processarWebhookPipefy"]["sucesso"] is False
    assert "não encontrado" in dados["data"]["processarWebhookPipefy"]["mensagem"].lower()


@pytest.mark.asyncio
async def test_webhook_prioridade_normal(client):
    """Cenário 4: Cliente com patrimônio < 200.000 deve ter prioridade normal."""
    mutation = """
        mutation {
          createCliente(input: {
            clienteName: "Cliente Prioridade Normal"
            clienteEmail: "prioridade_normal@example.com"
            tipoSolicitacao: "Test"
            valorPatrimonio: 100000.00
          }) {
            id
          }
        }
    """
    await client.post("/cliente", json={"query": mutation})

    webhook_mutation = """
        mutation {
          processarWebhookPipefy(input: {
            eventId: "evt_004"
            cardId: "card_004"
            clienteEmail: "prioridade_normal@example.com"
            timestamp: "2026-05-28T12:00:00Z"
          }) {
            sucesso
            prioridade
          }
        }
    """
    response = await client.post("/cliente", json={"query": webhook_mutation})
    dados = response.json()
    assert dados["data"]["processarWebhookPipefy"]["sucesso"] is True
    assert dados["data"]["processarWebhookPipefy"]["prioridade"] == "prioridade_normal"


@pytest.mark.asyncio
async def test_webhook_prioridade_alta(client):
    """Cenário 5: Cliente com patrimônio >= 200.000 deve ter prioridade alta."""
    mutation = """
        mutation {
          createCliente(input: {
            clienteName: "Cliente Prioridade Alta"
            clienteEmail: "prioridade_alta@example.com"
            tipoSolicitacao: "Test"
            valorPatrimonio: 300000.00
          }) {
            id
          }
        }
    """
    await client.post("/cliente", json={"query": mutation})

    webhook_mutation = """
        mutation {
          processarWebhookPipefy(input: {
            eventId: "evt_005"
            cardId: "card_005"
            clienteEmail: "prioridade_alta@example.com"
            timestamp: "2026-05-28T12:00:00Z"
          }) {
            sucesso
            prioridade
          }
        }
    """
    response = await client.post("/cliente", json={"query": webhook_mutation})
    dados = response.json()
    assert dados["data"]["processarWebhookPipefy"]["sucesso"] is True
    assert dados["data"]["processarWebhookPipefy"]["prioridade"] == "prioridade_alta"
