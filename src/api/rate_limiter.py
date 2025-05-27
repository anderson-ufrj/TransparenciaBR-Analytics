"""
Rate Limiter para controlar requisições à API.
"""

import asyncio
import time
from collections import deque
from datetime import datetime, timedelta
from threading import Lock
from typing import Optional

from loguru import logger


class RateLimiter:
    """
    Implementa rate limiting com janela deslizante.
    
    Limites:
    - 700 requisições/minuto entre 00:00 e 06:00
    - 400 requisições/minuto entre 06:00 e 24:00
    """
    
    def __init__(self):
        self.requests = deque()
        self.lock = Lock()
        self._last_cleanup = time.time()
        
    def get_current_limit(self) -> int:
        """Retorna o limite atual baseado no horário."""
        current_hour = datetime.now().hour
        if 0 <= current_hour < 6:
            return 700
        return 400
    
    def _cleanup_old_requests(self):
        """Remove requisições antigas da fila."""
        cutoff_time = time.time() - 60  # Janela de 1 minuto
        while self.requests and self.requests[0] < cutoff_time:
            self.requests.popleft()
    
    def can_make_request(self) -> bool:
        """Verifica se pode fazer uma requisição agora."""
        with self.lock:
            self._cleanup_old_requests()
            current_limit = self.get_current_limit()
            return len(self.requests) < current_limit
    
    def wait_if_needed(self) -> float:
        """
        Aguarda se necessário e retorna tempo de espera em segundos.
        """
        with self.lock:
            self._cleanup_old_requests()
            current_limit = self.get_current_limit()
            
            if len(self.requests) < current_limit:
                self.requests.append(time.time())
                return 0.0
            
            # Calcula tempo de espera
            oldest_request = self.requests[0]
            wait_time = 60 - (time.time() - oldest_request) + 0.1
            
            if wait_time > 0:
                logger.warning(
                    f"Rate limit atingido ({len(self.requests)}/{current_limit}). "
                    f"Aguardando {wait_time:.1f}s"
                )
                time.sleep(wait_time)
                
                # Tenta novamente após esperar
                self._cleanup_old_requests()
                self.requests.append(time.time())
                
            return wait_time
    
    def get_remaining_requests(self) -> int:
        """Retorna número de requisições disponíveis."""
        with self.lock:
            self._cleanup_old_requests()
            current_limit = self.get_current_limit()
            return max(0, current_limit - len(self.requests))
    
    def reset(self):
        """Reseta o rate limiter."""
        with self.lock:
            self.requests.clear()
            logger.info("Rate limiter resetado")


class AsyncRateLimiter:
    """Versão assíncrona do Rate Limiter."""
    
    def __init__(self):
        self.requests = deque()
        self.lock = asyncio.Lock()
        
    def get_current_limit(self) -> int:
        """Retorna o limite atual baseado no horário."""
        current_hour = datetime.now().hour
        if 0 <= current_hour < 6:
            return 700
        return 400
    
    async def _cleanup_old_requests(self):
        """Remove requisições antigas da fila."""
        cutoff_time = time.time() - 60
        while self.requests and self.requests[0] < cutoff_time:
            self.requests.popleft()
    
    async def wait_if_needed(self) -> float:
        """Aguarda se necessário (versão assíncrona)."""
        async with self.lock:
            await self._cleanup_old_requests()
            current_limit = self.get_current_limit()
            
            if len(self.requests) < current_limit:
                self.requests.append(time.time())
                return 0.0
            
            oldest_request = self.requests[0]
            wait_time = 60 - (time.time() - oldest_request) + 0.1
            
            if wait_time > 0:
                logger.warning(
                    f"Rate limit atingido ({len(self.requests)}/{current_limit}). "
                    f"Aguardando {wait_time:.1f}s"
                )
                await asyncio.sleep(wait_time)
                
                await self._cleanup_old_requests()
                self.requests.append(time.time())
                
            return wait_time