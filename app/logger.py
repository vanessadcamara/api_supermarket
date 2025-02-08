from loguru import logger
import sys

# Configuração do Loguru
logger.remove()  
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")  
logger.add("logs/app.log", rotation="10 MB", retention="10 days", level="DEBUG")

logger.info("O logger foi configurado.")