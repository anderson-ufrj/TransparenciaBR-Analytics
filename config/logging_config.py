"""
Configuração de logging para o projeto.
"""

import os
import sys
from pathlib import Path

from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def setup_logging():
    """Configura o sistema de logging usando loguru."""
    
    # Remove configurações padrão
    logger.remove()
    
    # Nível de log do ambiente
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "logs/transparencia.log")
    
    # Criar diretório de logs se não existir
    log_dir = Path(log_file).parent
    log_dir.mkdir(exist_ok=True)
    
    # Formato do log
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Console handler
    logger.add(
        sys.stdout,
        format=log_format,
        level=log_level,
        colorize=True
    )
    
    # File handler
    logger.add(
        log_file,
        format=log_format,
        level=log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True
    )
    
    # Handler específico para erros
    logger.add(
        log_file.replace(".log", "_errors.log"),
        format=log_format,
        level="ERROR",
        rotation="5 MB",
        retention="60 days",
        compression="zip",
        enqueue=True
    )
    
    # Log de início
    logger.info("Sistema de logging configurado com sucesso")
    logger.info(f"Nível de log: {log_level}")
    logger.info(f"Arquivo de log: {log_file}")
    
    return logger


# Configurar logging ao importar
configured_logger = setup_logging()