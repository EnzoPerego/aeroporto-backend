# Guia do Alembic

O schema do banco é definido pelas entities SQLAlchemy em `src/entities/` — nunca
escrevemos `CREATE TABLE` à mão. O Alembic gera as migrations automaticamente a
partir dessas entities (`--autogenerate`) e aplica no Postgres/Supabase.

`alembic/env.py` já está configurado para:
- Importar `Base.metadata` de `src/database/database.py` (via `src/entities/__init__.py`,
  que registra todas as entities)
- Ler a `DATABASE_URL` do `.env` (via `src/config/config.py`) em vez do `alembic.ini`

## Fluxo do dia a dia

1. Crie ou altere uma entity em `src/entities/`
2. Gere a migration comparando o banco atual com as entities:
   ```bash
   alembic revision --autogenerate -m "descricao da mudanca"
   ```
3. **Sempre abra o arquivo gerado em `alembic/versions/`** e confira se o
   `upgrade()`/`downgrade()` fazem sentido — autogenerate erra silenciosamente em
   casos como renomear coluna (ele vê como "remover + adicionar") ou alguns tipos
   customizados
4. Aplique no banco:
   ```bash
   alembic upgrade head
   ```

## Outros comandos úteis

```bash
alembic current          # qual migration está aplicada no banco agora
alembic history           # lista todas as migrations em ordem
alembic downgrade -1      # desfaz a última migration
alembic upgrade head      # aplica todas as migrations pendentes
```

## Primeira vez rodando o projeto

Depois de configurar o `.env` com a `DATABASE_URL`, rode:

```bash
alembic upgrade head    # cria todas as tabelas
python -m src.seed      # popula dados de exemplo (opcional)
```
