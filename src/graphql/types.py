import strawberry

#Estruturando o tipo de dados para o GraphQL
@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    is_active: bool


