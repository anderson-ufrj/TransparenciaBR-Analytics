"""
Configurações da API do Portal da Transparência.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class APIConfig:
    """Configurações para acesso à API do Portal da Transparência."""
    
    base_url: str = os.getenv("TRANSPARENCIA_BASE_URL", "http://api.portaldatransparencia.gov.br/api-de-dados")
    api_token: Optional[str] = os.getenv("TRANSPARENCIA_API_TOKEN")
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    cache_expiry_hours: int = int(os.getenv("CACHE_EXPIRY_HOURS", "24"))
    max_requests_per_minute: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "400"))
    
    # Rate limiting por horário
    rate_limits: Dict[str, int] = {
        "madrugada": 700,  # 00:00 - 06:00
        "diurno": 400      # 06:00 - 24:00
    }
    
    # Timeouts
    connection_timeout: int = 30
    read_timeout: int = 60
    
    # Retry configuration
    max_retries: int = 3
    backoff_factor: float = 1.5
    
    # Headers padrão
    default_headers: Dict[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "TransparenciaBR-Analytics/0.1.0"
    }
    
    def get_current_rate_limit(self) -> int:
        """Retorna o limite de requisições baseado no horário atual."""
        current_hour = datetime.now().hour
        if 0 <= current_hour < 6:
            return self.rate_limits["madrugada"]
        return self.rate_limits["diurno"]
    
    def get_headers(self) -> Dict[str, str]:
        """Retorna headers com token de autenticação se disponível."""
        headers = self.default_headers.copy()
        if self.api_token:
            headers["chave-api-dados"] = self.api_token
        return headers


# Instância global de configuração
api_config = APIConfig()