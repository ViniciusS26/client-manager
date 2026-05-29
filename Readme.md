# TESTE TÉCNICO: Desenvolvedor Backend (Client Management & Pipefy Integration)

Este projeto simula o  esqueleto de um sistema interno para o Mundo Invest. A aplicação  gerencia os  clientes e seus respectivos patrimônios investidos, além de mapear essas ações para o Pipefy.


## Instruções de execução do Projeto

### 1. Instruções de execução local do projeto e dos testes.

   - Crie e ative um ambiente virtual Python:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Instale as dependências:
     ```powershell
     pip install -r Requirements.txt
     ```
   - Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente do banco:
     ```text
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=postgres
     POSTGRES_DB=teste_mundo_inv
     POSTGRES_HOST=localhost
     POSTGRES_PORT=5432
     DATABASE_URL=postgresql://postgres:postgres@localhost:5432/teste_mundo_inv
     ```
  
   - Execute os testes:
     ```powershell
     python -m pytest -v
     ```

   #### Execução com Docker

   - Levante os containers:
     ```powershell
     docker compose up -d
     ```
   - Execute os testes dentro do container `api`:
     ```powershell
     docker compose exec api python -m pytest -v
     ```
   - Acesse a API no navegador ou via `curl` em:
     ```text
     http://localhost:8000
     ```

### 2. Exemplos de requisição (`curl`) para os dois endpoints.

   - Endpoint GraphQL para criar cliente (Linux/macOS):
     ```bash
     curl -X POST http://localhost:8000/cliente \
       -H "Content-Type: application/json" \
       -d '{"query":"mutation { createCliente(input: { clienteName: \"Cliente Teste\" clienteEmail: \"teste@example.com\" tipoSolicitacao: \"Teste\" valorPatrimonio: 150000.00 }) { id clienteName prioridade } }"}'
     ```

   - Endpoint GraphQL para criar cliente (Windows PowerShell):
     ```powershell
     curl.exe -X POST http://localhost:8000/cliente `
       -H "Content-Type: application/json" `
       -d '{"query":"mutation { createCliente(input: { clienteName: \"Cliente Teste\" clienteEmail: \"teste@example.com\" tipoSolicitacao: \"Teste\" valorPatrimonio: 150000.00 }) { id clienteName prioridade } }"}'
     ```

   - Endpoint REST para webhook Pipefy (Linux/macOS):
     ```bash
     curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
       -H "Content-Type: application/json" \
       -d '{"event_id":"evt_001","card_id":"card_001","cliente_email":"teste@example.com","timestamp":"2026-05-29T12:00:00Z"}'
     ```

   - Endpoint REST para webhook Pipefy (Windows PowerShell):
     ```powershell
     curl.exe -X POST http://localhost:8000/webhooks/pipefy/card-updated `
       -H "Content-Type: application/json" `
       -d '{"event_id":"evt_001","card_id":"card_001","cliente_email":"teste@example.com","timestamp":"2026-05-29T12:00:00Z"}'
     ```

   - Query GraphQL `get_clientes` (Linux/macOS):
     ```bash
     curl -X POST http://localhost:8000/cliente \
       -H "Content-Type: application/json" \
       -d '{"query":"query { get_clientes { id clienteName clienteEmail tipoSolicitacao valorPatrimonio status prioridade } }"}'
     ```

   - Query GraphQL `get_clientes` (Windows PowerShell):
     ```powershell
     curl.exe -X POST http://localhost:8000/cliente `
       -H "Content-Type: application/json" `
       -d '{"query":"query { get_clientes { id clienteName clienteEmail tipoSolicitacao valorPatrimonio status prioridade } }"}'
     ```

### 3 Tecnologias usadas

- 🐍 Python 3.10
- 🚀 FastAPI
- 🍓 Strawberry GraphQL
- 🧠 SQLAlchemy
- 🐘 AsyncPG / PostgreSQL
- 🔧 Pydantic
- ✅ pytest
- 🐳 Docker / Docker Compose
