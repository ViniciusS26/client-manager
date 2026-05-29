import pytest


@pytest.mark.asyncio
async def test_query_get_clientes_retorna_lista_vazia(client):
    """Quando não há clientes cadastrados, a query deve retornar uma lista vazia."""
    query = """
        query {
          getClientes {
            id
            clienteName
            clienteEmail
            tipoSolicitacao
            valorPatrimonio
            status
            prioridade
          }
        }
    """

    response = await client.post("/cliente", json={"query": query})
    assert response.status_code == 200

    dados = response.json()
    assert "errors" not in dados
    assert dados["data"]["getClientes"] == []


@pytest.mark.asyncio
async def test_query_get_clientes_retorna_clientes_cadastrados(client):
    """A query deve retornar os clientes cadastrados no banco."""
    create_mutation = """
        mutation {
          createCliente(input: {
            clienteName: "Cliente Query Test"
            clienteEmail: "query@teste.com"
            tipoSolicitacao: "Análise"
            valorPatrimonio: 120000.00
          }) {
            id
            clienteName
            clienteEmail
            status
            prioridade
          }
        }
    """

    create_response = await client.post("/cliente", json={"query": create_mutation})
    assert create_response.status_code == 200
    create_data = create_response.json()
    assert "errors" not in create_data

    query = """
        query {
          getClientes {
            id
            clienteName
            clienteEmail
            tipoSolicitacao
            valorPatrimonio
            status
            prioridade
          }
        }
    """

    response = await client.post("/cliente", json={"query": query})
    assert response.status_code == 200

    dados = response.json()
    assert "errors" not in dados
    clientes = dados["data"]["getClientes"]
    assert len(clientes) == 1
    assert clientes[0]["clienteName"] == "Cliente Query Test"
    assert clientes[0]["clienteEmail"] == "query@teste.com"
    assert clientes[0]["status"] == "Aguardando análise"
