from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.controllers import sales_router
from app.jobs import start_scheduler, start_aggregated_table_scheduler, update_product_sales_aggregated, update_category_revenue_aggregated, update_top_customers_aggregated
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the application...")

    # Atualiza a tabela de agregação imediatamente ao iniciar
    logger.info("Running initial update of aggregation table...")
    update_product_sales_aggregated()
    update_category_revenue_aggregated()
    update_top_customers_aggregated()

    # Inicia os jobs agendados
    start_scheduler()
    start_aggregated_table_scheduler()
    logger.info("Scheduler started.")
    
    yield  # Aqui a aplicação continua rodando
    logger.info("Stopping the application...")


app = FastAPI(lifespan=lifespan)

# Incluindo as rotas no FastAPI
app.include_router(sales_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
