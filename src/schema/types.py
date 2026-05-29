import strawberry

#Estruturando o tipo de dados para o GraphQL
@strawberry.type
class UserType:
    id: int
    cliente_name: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: str


from typing import Optional

@strawberry.type
class WebhookResultType:
    sucesso: bool
    mensagem: str
    cliente_id: Optional[int] = None
    prioridade: Optional[str] = None
    status: Optional[str] = None
