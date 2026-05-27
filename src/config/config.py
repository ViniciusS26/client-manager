# config.py
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configurações para a aplicação, incluindo as credenciais do banco de dados e a URL de conexão"""
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "db"
    postgres_port: int = 5432

    # Cria a URL final de conexão dinamicamente
    @computed_field
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # Configuração para ler do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instancia as configurações para serem usadas no projeto
settings = Settings()