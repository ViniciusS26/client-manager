import strawberry
from typing import List
from graphql.types import UserType

#querys para consultar os dados do banco de dados, utilizando o UserType para estruturar a resposta


@strawberry.type
class UserQuery:

    @strawberry.field
    def users(self) -> List[UserType]:
        
        return [
            UserType(id=1, name="Alice", email="alice@example.com", is_active=True),
            UserType(id=2, name="Bob", email="bob@example.com", is_active=False)
        ]