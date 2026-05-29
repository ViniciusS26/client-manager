import strawberry
from strawberry.types import Info
from sqlalchemy.future import select

from pydantic import BaseModel, EmailStr, Field, field_validator
from email_validator import validate_email, EmailNotValidError
from src.connection.connection import AsyncSessionLocal
from src.models.models import Cliente


class ClienteValidator(BaseModel):
    """ 
        Validações para os campos de entrada, como tipo de solicitação e valor do patrimônio.
    """
    cliente_name: str = Field(..., min_length=1, max_length=100)
    cliente_email: EmailStr
    tipo_solicitacao: str = Field(..., min_length=1, max_length=50)
    valor_patrimonio: float = Field(..., gt=0)

    """Validar se todos os campos estão preenchidos"""
    @field_validator('cliente_email', 'tipo_solicitacao', 'valor_patrimonio')
    def validate_not_empty(cls, value, field):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"O campo {field.name} não pode estar vazio.")
        return value

    """Validar se o email é válido"""
    @field_validator('cliente_email')
    def validate_cliente_email(cls, value):
       
        try:
            validate_email(value, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(f"Email inválido: {e}")

        return value

    @field_validator('valor_patrimonio')
    def validate_valor_patrimonio(cls, value):
        if value <= 0:
            raise ValueError("O valor do patrimônio deve ser um número positivo.")
        return value



"""
FUNÇÕES SEPARADAS PARA VALIDAÇÃO
"""

def valida_dados(cliente: Cliente):
    """Função para validar os dados de entrada utilizando o ClienteValidator"""
    try:
        cliente_validado = ClienteValidator(
            cliente_name=cliente.cliente_name,
            cliente_email=cliente.cliente_email,
            tipo_solicitacao=cliente.tipo_solicitacao,
            valor_patrimonio=cliente.valor_patrimonio
        )
        return cliente_validado
    except ValueError as e:
        raise ValueError(str(e))


async def verifica_email(cliente_email: str) -> bool:
    """Função para verificar se o email já existe no banco de dados"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Cliente).where(Cliente.cliente_email == cliente_email))
        cliente = result.scalars().first()
        return cliente is not None