# Usa uma imagem oficial do Python otimizada
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Evita que o Python escreva arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE 1
# Garante que a saída do console seja exibida em tempo real
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias para compilar pacotes (como psycopg2 para o Postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependências primeiro (otimiza o cache do Docker)
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o container
COPY . .

# Expõe a porta que o FastAPI/Uvicorn vai rodar
EXPOSE 8000

# O comando padrão será sobrescrito pelo docker-compose em desenvolvimento,
# mas serve como um excelente fallback para produção
CMD ["uvicorn", "schemas:app", "--host", "0.0.0.0", "--port", "8000"]