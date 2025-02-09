from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.controllers import sales_router
from app.jobs import start_scheduler, start_aggregated_table_scheduler, update_product_sales_aggregated
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Gerencia o ciclo de vida da aplicação """

    logger.info("Iniciando a aplicação...")

    # Atualiza a tabela de agregação imediatamente ao iniciar
    logger.info("Executando a atualização inicial da tabela de agregação...")
    update_product_sales_aggregated()

    # Inicia os jobs agendados
    start_scheduler()
    start_aggregated_table_scheduler()

    logger.info("Aplicação iniciada e scheduler rodando.")
    
    yield  # Aqui a aplicação continua rodando

    logger.info("Finalizando a aplicação...")


app = FastAPI(lifespan=lifespan)

# Incluindo as rotas no FastAPI
app.include_router(sales_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
