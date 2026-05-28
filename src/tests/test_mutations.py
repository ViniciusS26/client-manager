import pytest

@pytest.mark.asyncio
async def test_cadastrar_cliente_sucesso(client):
    """Cenário 1: Cadastro com dados perfeitos deve retornar o cliente criado."""
    mutation = """
        mutation {
          createCliente(input: {
            clienteName: "Vinicius Nunes"
            clienteEmail: "vinicius@teste.com"
            tipoSolicitacao: "Abertura de Conta"
            valorPatrimonio: 50000.00
          }) {
            id
            clienteName
            clienteEmail
          }
        }
    """
    response = await client.post("/cliente", json={"query": mutation})
    assert response.status_code == 200

    dados = response.json()
    assert "errors" not in dados
    assert dados["data"]["createCliente"]["clienteName"] == "Vinicius Nunes"
    assert dados["data"]["createCliente"]["id"] is not None


@pytest.mark.asyncio
async def test_cadastrar_cliente_erro_validacao(client):
    """Cenário 2: Enviar valor de patrimônio negativo deve retornar erro de validação."""
    mutation = """
        mutation {
          createCliente(input: {
            clienteName: "João"
            clienteEmail: "joao@teste.com"
            tipoSolicitacao: "Suporte"
            valorPatrimonio: -100.00
          }) {
            id
          }
        }
    """
    response = await client.post("/cliente", json={"query": mutation})
    assert response.status_code == 200

    dados = response.json()
    assert dados["data"] is None
    assert "errors" in dados
    assert "greater than 0" in dados["errors"][0]["message"].lower()


@pytest.mark.asyncio
async def test_cadastrar_cliente_email_duplicado(client):
    """Cenário 3: Tentar cadastrar o mesmo e-mail duas vezes deve disparar o erro de negócio."""
    mutation = """
        mutation {
          createCliente(input: {
            clienteName: "Cliente Original"
            clienteEmail: "duplicado@teste.com"
            tipoSolicitacao: "Suporte"
            valorPatrimonio: 1000.00
          }) {
            id
          }
        }
    """

    response1 = await client.post("/cliente", json={"query": mutation})
    assert "errors" not in response1.json()

    response2 = await client.post("/cliente", json={"query": mutation})
    dados_erro = response2.json()

    assert dados_erro["data"] is None
    assert "errors" in dados_erro
    assert "já está cadastrado" in dados_erro["errors"][0]["message"]
