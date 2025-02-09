from alembic import op
import sys
import time
from sqlalchemy import text
from typing import Sequence, Union


# Identificação da revisão Alembic
revision: str = '02346e154b7d'
down_revision: Union[str, None] = '72618bb5f2c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def log_message(message: str):
    """ Exibe logs imediatamente no console. """
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()


def upgrade():
    start_time = time.time()
    log_message(f"Iniciando migração no tempo: {start_time}")

    # Criar a tabela particionada
    log_message("Criando tabela particionada sales_new...")
    op.execute("""
        CREATE TABLE IF NOT EXISTS sales_new (
            id SERIAL,
            id_user INTEGER NOT NULL,
            datetime TIMESTAMP NOT NULL,
            CONSTRAINT sales_new_pkey PRIMARY KEY (id, datetime),
            CONSTRAINT sales_new_id_user_fkey FOREIGN KEY (id_user)
                REFERENCES users (id) ON DELETE NO ACTION
        ) PARTITION BY RANGE (datetime);
    """)
    log_message("Tabela sales_new criada.")

    # Criar partições mensais de 2020 a 2025
    for year in range(2020, 2026):
        log_message(f"Criando partições para o ano {year}...")
        for month in range(1, 13):
            start_date = f"'{year}-{month:02d}-01'"
            end_date = f"'{year}-{month+1:02d}-01'" if month < 12 else f"'{year+1}-01-01'"
            partition_name = f"sales_{year}_{month:02d}"
            op.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {partition_name} PARTITION OF sales_new
                FOR VALUES FROM ({start_date}) TO ({end_date});
            """))
        log_message(f"Partições do ano {year} criadas.")

    # Criar índices
    log_message("Criando índices na tabela particionada...")
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_sales_new_datetime ON sales_new (datetime);
        CREATE INDEX IF NOT EXISTS idx_sales_new_id_user ON sales_new (id_user);
    """)
    log_message("Índices criados.")

    log_message(f"Finalizando migração em {round(time.time() - start_time, 2)} segundos.")


def downgrade():
    log_message("Iniciando reversão da migração.")

    # Restaurar a tabela original
    log_message("Criando tabela sales original.")
    op.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            id_user INTEGER NOT NULL,
            datetime TIMESTAMP NOT NULL,
            CONSTRAINT sales_id_user_fkey FOREIGN KEY (id_user)
                REFERENCES users (id) ON DELETE NO ACTION
        );
    """)

    # Restaurar os dados da partição para a tabela normal
    log_message("Restaurando dados da partição para a tabela normal.")
    op.execute("""
        INSERT INTO sales (id, id_user, datetime)
        SELECT id, id_user, datetime FROM sales_new;
    """)

    # Remover partições
    log_message("Removendo partições.")
    for year in range(2020, 2026):
        for month in range(1, 13):
            partition_name = f"sales_{year}_{month:02d}"
            op.execute(text(f"DROP TABLE IF EXISTS {partition_name} CASCADE;"))

    # Remover a tabela particionada
    log_message("Removendo tabela particionada.")
    op.execute("DROP TABLE IF EXISTS sales_new CASCADE;")

    log_message("Downgrade concluído.")
