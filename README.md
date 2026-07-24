# Aeroporto - Backend

API REST (FastAPI + PostgreSQL/Supabase) para a plataforma de gestão operacional de aeroporto.

Projeto de capacitação técnica.

## Entidades

`terminais`, `gates`, `aeronaves`, `voos`, `passageiros`, `reservas` (liga passageiro↔voo,
resolvendo o N:N e guardando status de check-in/realocação) e `malas` (associadas a uma
reserva). O schema é definido pelas entities SQLAlchemy em `src/entities/` e versionado
via Alembic — sem SQL manual (ver [ALEMBIC_GUIDE.md](ALEMBIC_GUIDE.md)).

## Estrutura

```
src/
  app.py              # entrypoint FastAPI
  config/              # leitura de variáveis de ambiente
  database/            # engine/session SQLAlchemy
  entities/             # models SQLAlchemy (schema do banco)
  models/               # schemas Pydantic (request/response)
  repositories/         # acesso a dados (uma classe por entidade)
  use_cases/            # regras de negócio, organizadas por domínio
  routers/              # endpoints HTTP, chamam use_cases
alembic/                 # migrations
```

Padrão de camadas: `router` recebe a requisição HTTP → chama um `use_case` → que usa
um ou mais `repository` para acessar o banco. `entities` (SQLAlchemy) e `models`
(Pydantic) ficam separados de propósito: entities descrevem o banco, models descrevem
o contrato da API.

## Setup

```bash
./setup.sh
# ou manualmente:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # preencha DATABASE_URL com a connection string do Supabase
alembic upgrade head    # cria as tabelas
```

## Rodar

```bash
source .venv/bin/activate
uvicorn src.app:app --reload
```

A API sobe em `http://localhost:8000`. Documentação interativa em `/docs`.

## Migrations

Ver [ALEMBIC_GUIDE.md](ALEMBIC_GUIDE.md) para o fluxo completo.

## Popular com dados de exemplo (opcional)

```bash
source .venv/bin/activate
python -m src.seed
```
