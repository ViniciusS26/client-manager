import typing
import strawberry
"""
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}
"""


@strawberry.type
class Cliente:
    cliente_name: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float


def get_cliente() -> Cliente:
    return Cliente(
        cliente_name="João Silva",
        cliente_email="joao.silva@example.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=250000.0
    )



