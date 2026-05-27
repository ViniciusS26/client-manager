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


