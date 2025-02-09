from alembic import op
import sys
import time
from sqlalchemy import text
from typing import Sequence, Union


# Identificação da revisão Alembic
revision: str = '0bf171014049'
down_revision: Union[str, None] = '02346e154b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def log_message(message: str):
    """ Exibe logs imediatamente no console. """
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()


def upgrade():
    start_time = time.time()
    log_message("Iniciando migração dos dados da tabela sales para sales_new.")

    # Definir tamanho do lote para migração
    batch_size = 100_000

    # Obter conexão com o banco
    conn = op.get_bind()

    # Obter o menor e maior ID da tabela sales
    log_message("Obtendo intervalo de IDs para migração...")
    min_max_result = conn.execute(text("SELECT MIN(id), MAX(id) FROM sales")).fetchone()
    min_id, max_id = min_max_result if min_max_result else (None, None)

    if min_id is None or max_id is None:
        log_message("Nenhum dado encontrado na tabela sales. Nada para migrar.")
    else:
        total_rows = conn.execute(text("SELECT COUNT(*) FROM sales")).scalar()
        log_message(f"Total de registros a serem migrados: {total_rows}")

        migrated_rows = 0
        current_id = min_id

        while current_id <= max_id:
            conn.execute(text("""
                INSERT INTO sales_new (id, id_user, datetime)
                SELECT id, id_user, datetime FROM sales
                WHERE id >= :start_id AND id < :end_id;
            """), {"start_id": current_id, "end_id": current_id + batch_size})

            current_id += batch_size
            migrated_rows += batch_size
            log_message(f"Migrados {min(migrated_rows, total_rows)} de {total_rows} registros.")

    log_message(f"Migração concluída em {round(time.time() - start_time, 2)} segundos.")


def downgrade():
    log_message("Revertendo migração de dados...")

    log_message("Removendo registros migrados da tabela sales_new.")
    conn = op.get_bind()
    conn.execute(text("DELETE FROM sales_new;"))

    log_message("Downgrade concluído.")
