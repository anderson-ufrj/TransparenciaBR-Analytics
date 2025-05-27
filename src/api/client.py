"""
Robust API client for Portal da Transparência with rate limiting, caching, and retry logic.
"""

import os
import time
import json
import hashlib
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import urljoin
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter implementation."""
    
    def __init__(self, max_calls: int = 30, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = []
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside the window
            self.calls = [call_time for call_time in self.calls 
                          if now - call_time < self.window_seconds]
            
            # Check if we've exceeded the rate limit
            if len(self.calls) >= self.max_calls:
                sleep_time = self.window_seconds - (now - self.calls[0])
                logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                # Retry after sleeping
                return wrapper(*args, **kwargs)
            
            # Record this call and proceed
            self.calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper


class CacheManager:
    """Simple file-based cache manager."""
    
    def __init__(self, cache_dir: str = "data/cache", ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self.enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    
    def _get_cache_key(self, url: str, params: Dict[str, Any]) -> str:
        """Generate a cache key from URL and parameters."""
        cache_string = f"{url}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Retrieve data from cache if available and not expired."""
        if not self.enabled:
            return None
            
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                # Check if cache is still valid
                cached_time = datetime.fromisoformat(cached_data['cached_at'])
                if datetime.now() - cached_time < timedelta(seconds=self.ttl):
                    logger.debug(f"Cache hit for {url}")
                    return cached_data['data']
                else:
                    logger.debug(f"Cache expired for {url}")
                    cache_file.unlink()
            except Exception as e:
                logger.error(f"Error reading cache: {e}")
        
        return None
    
    def set(self, url: str, params: Dict[str, Any], data: Dict[str, Any]) -> None:
        """Store data in cache."""
        if not self.enabled:
            return
            
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            cached_data = {
                'cached_at': datetime.now().isoformat(),
                'url': url,
                'params': params,
                'data': data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Data cached for {url}")
        except Exception as e:
            logger.error(f"Error writing cache: {e}")


class TransparenciaAPIClient:
    """
    Robust client for Portal da Transparência API.
    
    Features:
    - Automatic rate limiting (30 requests/minute)
    - Exponential backoff retry logic
    - Intelligent caching with configurable TTL
    - Comprehensive error handling
    - Detailed logging
    """
    
    BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
    
    # API Endpoints
    ENDPOINTS = {
        # Despesas
        "despesas_contratos": "/contratos",
        "despesas_convenios": "/convenios",
        "despesas_cartoes": "/cartoes",
        "despesas_cpgf": "/cpgf",
        "despesas_cpcc": "/cpcc",
        "despesas_documentos": "/documentos",
        "despesas_empenhos": "/empenhos",
        "despesas_liquidacoes": "/liquidacoes",
        "despesas_pagamentos": "/pagamentos",
        
        # Receitas
        "receitas_previstas": "/receitas/previstas",
        "receitas_realizadas": "/receitas/realizadas",
        
        # Servidores
        "servidores": "/servidores",
        "servidores_por_orgao": "/servidores/por-orgao",
        "servidores_remuneracao": "/servidores/remuneracao",
        
        # Benefícios
        "beneficios_auxilio_brasil": "/auxilio-brasil",
        "beneficios_bolsa_familia": "/bolsa-familia-disponivel",
        "beneficios_bpc": "/bpc",
        "beneficios_seguro_defeso": "/seguro-defeso",
        
        # Licitações
        "licitacoes": "/licitacoes",
        
        # Sanções
        "sancoes_ceis": "/ceis",
        "sancoes_cepim": "/cepim",
        "sancoes_ceaf": "/ceaf",
        "sancoes_cnep": "/cnep",
        
        # Órgãos
        "orgaos_siafi": "/orgaos-siafi",
        "orgaos_siape": "/orgaos-siape",
        
        # Fornecedores
        "fornecedores": "/fornecedores",
    }
    
    def __init__(self):
        """Initialize the API client with configuration from environment."""
        self.api_token = os.getenv("TRANSPARENCIA_API_TOKEN")
        self.api_email = os.getenv("TRANSPARENCIA_API_EMAIL")
        
        if not self.api_token:
            raise ValueError("TRANSPARENCIA_API_TOKEN not found in environment variables")
        
        # Configuration
        self.rate_limit = int(os.getenv("API_RATE_LIMIT", "30"))
        self.timeout = int(os.getenv("API_TIMEOUT", "60"))
        self.cache_ttl = int(os.getenv("CACHE_TTL", "3600"))
        
        # Setup components
        self.session = self._setup_session()
        self.rate_limiter = RateLimiter(max_calls=self.rate_limit)
        self.cache = CacheManager(ttl=self.cache_ttl)
        
        # Configure logging
        log_level = os.getenv("LOG_LEVEL", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        logger.info("TransparenciaAPIClient initialized successfully")
    
    def _setup_session(self) -> requests.Session:
        """Setup requests session with retry logic and connection pooling."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            "chave-api-dados": self.api_token,
            "Accept": "application/json",
            "User-Agent": f"TransparenciaBR-Analytics/1.0 ({self.api_email})"
        })
        
        return session
    
    @RateLimiter()
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make HTTP request with rate limiting and error handling.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            requests.RequestException: For HTTP errors
            ValueError: For invalid responses
        """
        url = urljoin(self.BASE_URL, endpoint)
        params = params or {}
        
        # Check cache first
        cached_data = self.cache.get(url, params)
        if cached_data is not None:
            return cached_data
        
        logger.info(f"Making request to {endpoint} with params: {params}")
        
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            
            # Log response details
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            # Check for rate limit headers
            if 'X-Rate-Limit-Remaining' in response.headers:
                remaining = response.headers['X-Rate-Limit-Remaining']
                logger.info(f"Rate limit remaining: {remaining}")
            
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Cache the successful response
            self.cache.set(url, params, data)
            
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for {url}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e.response.text}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON response from {url}")
            raise ValueError("Invalid JSON response from API")
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test API connection and authentication.
        
        Returns:
            True if connection is successful
        """
        try:
            # Test with a simple endpoint
            self._make_request("/orgaos-siafi", {"pagina": 1, "quantidade": 1})
            logger.info("API connection test successful")
            return True
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False
    
    # Despesas methods
    def get_contratos(self, **params) -> List[Dict[str, Any]]:
        """Buscar contratos."""
        return self._make_request(self.ENDPOINTS["despesas_contratos"], params)
    
    def get_convenios(self, **params) -> List[Dict[str, Any]]:
        """Buscar convênios."""
        return self._make_request(self.ENDPOINTS["despesas_convenios"], params)
    
    def get_cartoes(self, **params) -> List[Dict[str, Any]]:
        """Buscar despesas com cartões."""
        return self._make_request(self.ENDPOINTS["despesas_cartoes"], params)
    
    def get_empenhos(self, **params) -> List[Dict[str, Any]]:
        """Buscar empenhos."""
        return self._make_request(self.ENDPOINTS["despesas_empenhos"], params)
    
    def get_pagamentos(self, **params) -> List[Dict[str, Any]]:
        """Buscar pagamentos."""
        return self._make_request(self.ENDPOINTS["despesas_pagamentos"], params)
    
    # Receitas methods
    def get_receitas_previstas(self, **params) -> List[Dict[str, Any]]:
        """Buscar receitas previstas."""
        return self._make_request(self.ENDPOINTS["receitas_previstas"], params)
    
    def get_receitas_realizadas(self, **params) -> List[Dict[str, Any]]:
        """Buscar receitas realizadas."""
        return self._make_request(self.ENDPOINTS["receitas_realizadas"], params)
    
    # Servidores methods
    def get_servidores(self, **params) -> List[Dict[str, Any]]:
        """Buscar servidores públicos."""
        return self._make_request(self.ENDPOINTS["servidores"], params)
    
    def get_servidores_remuneracao(self, **params) -> List[Dict[str, Any]]:
        """Buscar remuneração de servidores."""
        return self._make_request(self.ENDPOINTS["servidores_remuneracao"], params)
    
    # Benefícios methods
    def get_bolsa_familia(self, **params) -> List[Dict[str, Any]]:
        """Buscar beneficiários do Bolsa Família."""
        return self._make_request(self.ENDPOINTS["beneficios_bolsa_familia"], params)
    
    def get_auxilio_brasil(self, **params) -> List[Dict[str, Any]]:
        """Buscar beneficiários do Auxílio Brasil."""
        return self._make_request(self.ENDPOINTS["beneficios_auxilio_brasil"], params)
    
    # Licitações methods
    def get_licitacoes(self, **params) -> List[Dict[str, Any]]:
        """Buscar licitações."""
        return self._make_request(self.ENDPOINTS["licitacoes"], params)
    
    # Sanções methods
    def get_empresas_sancionadas(self, tipo: str = "ceis", **params) -> List[Dict[str, Any]]:
        """
        Buscar empresas sancionadas.
        
        Args:
            tipo: Tipo de sanção (ceis, cepim, ceaf, cnep)
            **params: Parâmetros adicionais da consulta
        """
        endpoint_key = f"sancoes_{tipo}"
        if endpoint_key not in self.ENDPOINTS:
            raise ValueError(f"Tipo de sanção inválido: {tipo}")
        
        return self._make_request(self.ENDPOINTS[endpoint_key], params)
    
    # Órgãos methods
    def get_orgaos(self, sistema: str = "siafi", **params) -> List[Dict[str, Any]]:
        """
        Buscar órgãos.
        
        Args:
            sistema: Sistema de origem (siafi ou siape)
            **params: Parâmetros adicionais da consulta
        """
        endpoint_key = f"orgaos_{sistema}"
        if endpoint_key not in self.ENDPOINTS:
            raise ValueError(f"Sistema inválido: {sistema}")
        
        return self._make_request(self.ENDPOINTS[endpoint_key], params)
    
    # Fornecedores methods
    def get_fornecedores(self, **params) -> List[Dict[str, Any]]:
        """Buscar fornecedores."""
        return self._make_request(self.ENDPOINTS["fornecedores"], params)
    
    # Utility methods
    def paginate(self, method: callable, max_pages: Optional[int] = None, 
                 page_size: int = 500, **params) -> List[Dict[str, Any]]:
        """
        Paginate through API results.
        
        Args:
            method: API method to call
            max_pages: Maximum number of pages to fetch (None for all)
            page_size: Number of items per page
            **params: Additional parameters for the API call
            
        Returns:
            Combined list of all results
        """
        all_results = []
        page = 1
        
        while True:
            try:
                params['pagina'] = page
                params['quantidade'] = page_size
                
                logger.info(f"Fetching page {page}")
                results = method(**params)
                
                if not results:
                    break
                    
                all_results.extend(results)
                
                if max_pages and page >= max_pages:
                    break
                    
                page += 1
                
            except Exception as e:
                logger.error(f"Error on page {page}: {e}")
                break
        
        logger.info(f"Fetched {len(all_results)} total results across {page-1} pages")
        return all_results
    
    def get_available_endpoints(self) -> Dict[str, str]:
        """Return all available API endpoints."""
        return self.ENDPOINTS.copy()
    
    def clear_cache(self) -> None:
        """Clear all cached data."""
        cache_dir = Path("data/cache")
        if cache_dir.exists():
            for cache_file in cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("Cache cleared successfully")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics."""
        cache_dir = Path("data/cache")
        cache_count = len(list(cache_dir.glob("*.json"))) if cache_dir.exists() else 0
        
        return {
            "rate_limit": self.rate_limit,
            "timeout": self.timeout,
            "cache_ttl": self.cache_ttl,
            "cache_enabled": self.cache.enabled,
            "cached_items": cache_count,
            "endpoints_available": len(self.ENDPOINTS)
        }