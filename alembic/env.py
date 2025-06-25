from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from tenants.models import Tenant
import sys
import os
from dotenv import load_dotenv

# Garante acesso ao seu app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Carrega as configs reais do projeto
from core.config import DATABASE_URL, Base

load_dotenv()

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Corrigir aqui 👇
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Rodar migrações no modo offline"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Rodar migrações no modo online"""
    from sqlalchemy import create_engine
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Decide entre offline e online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
