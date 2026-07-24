# Aeroporto - Backend

API REST (FastAPI + PostgreSQL/Supabase) para a plataforma de gestão operacional de aeroporto.

Projeto de capacitação técnica.

## Entidades

`terminais`, `gates`, `aeronaves`, `voos`, `passageiros`, `reservas` (liga passageiro↔voo,
resolvendo o N:N e guardando status de check-in/realocação) e `malas` (associadas a uma
reserva). As tabelas são criadas a partir dos models SQLAlchemy em `app/models/`, sem SQL
manual — ver `app/database.py` (`Base.metadata.create_all` roda no startup da API).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # preencha DATABASE_URL com a connection string do Supabase
```

## Rodar

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. Documentação interativa em `/docs`.

## Popular com dados de exemplo (opcional)

```bash
source .venv/bin/activate
python -m app.seed
```
