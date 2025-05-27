# 🛠️ Guia de Desenvolvimento

Este documento contém informações para desenvolvedores que desejam contribuir com o projeto TransparenciaBR-Analytics.

## 🏗️ Arquitetura do Projeto

### Visão Geral

```
TransparenciaBR-Analytics/
├── src/                     # Código fonte principal
│   ├── api/                # Cliente da API do Portal da Transparência
│   │   ├── __init__.py
│   │   └── client.py       # Cliente principal com rate limiting e cache
│   ├── data/               # Pipeline de processamento de dados
│   │   ├── __init__.py
│   │   ├── collector.py    # Coleta automatizada de dados
│   │   └── processor.py    # Limpeza e transformação
│   ├── dashboard/          # Interface Streamlit
│   │   ├── app.py         # Aplicação principal
│   │   └── pages/         # Páginas do dashboard
│   ├── models/            # Modelos de Machine Learning
│   └── utils/             # Funções auxiliares
├── tests/                 # Testes automatizados
├── data/                  # Dados coletados e processados
├── notebooks/            # Análises exploratórias
└── scripts/              # Scripts utilitários
```

### Componentes Principais

#### 1. Cliente da API (`src/api/client.py`)

```python
class TransparenciaAPIClient:
    """Cliente principal para acessar a API do Portal da Transparência"""
    
    def __init__(self, api_token: str, email: str, requests_per_minute: int = 30):
        self.rate_limiter = RateLimiter(requests_per_minute)
        self.cache_manager = CacheManager()
        self.session = self._create_session()
```

**Responsabilidades:**
- Gerenciar autenticação com a API
- Implementar rate limiting (30 req/min)
- Cache inteligente com TTL
- Retry automático com backoff exponencial
- Tratamento de erros HTTP

#### 2. Pipeline de Dados (`src/data/`)

**DataCollector (`collector.py`):**
```python
class DataCollector:
    """Coleta automatizada de dados da API"""
    
    def collect_gastos_periodo(self, orgaos: List[str], inicio: date, fim: date)
    def collect_contratos_periodo(self, orgaos: List[str], inicio: date, fim: date)
    def collect_fornecedores_ativos(self)
```

**DataProcessor (`processor.py`):**
```python
class DataProcessor:
    """Processamento e limpeza de dados"""
    
    def clean_gastos_data(self, df: pd.DataFrame) -> pd.DataFrame
    def normalize_values(self, df: pd.DataFrame) -> pd.DataFrame
    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame
```

#### 3. Dashboard (`src/dashboard/`)

Interface web construída com Streamlit:
- **app.py**: Aplicação principal com navegação
- **pages/**: Páginas individuais do dashboard
- Tema visual brasileiro com cores verde/amarelo

## 🚀 Configuração do Ambiente de Desenvolvimento

### 1. Clone e Configuração Inicial

```bash
# Clone o repositório
git clone https://github.com/anderson-ufrj/TransparenciaBR-Analytics.git
cd TransparenciaBR-Analytics

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências de desenvolvimento
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Se existir
```

### 2. Configuração de Ambiente

```bash
# Copie o template de configuração
cp .env.template .env

# Edite .env com suas credenciais
TRANSPARENCIA_API_TOKEN=seu_token_aqui
TRANSPARENCIA_EMAIL=seu_email@exemplo.com
```

### 3. Validação da Configuração

```bash
# Execute o script de validação
python scripts/validate_setup.py

# Teste a conectividade da API
python -c "
from src.api.client import TransparenciaAPIClient
import os
client = TransparenciaAPIClient(
    os.getenv('TRANSPARENCIA_API_TOKEN'),
    os.getenv('TRANSPARENCIA_EMAIL')
)
print('API conectada!' if client.health_check() else 'Erro na API')
"
```

## 🧪 Testes

### Estrutura de Testes

```
tests/
├── unit/                  # Testes unitários
│   ├── test_api_client.py
│   ├── test_data_processor.py
│   └── test_utils.py
├── integration/           # Testes de integração
│   ├── test_api_integration.py
│   └── test_data_pipeline.py
└── fixtures/             # Dados de teste
    ├── sample_gastos.json
    └── sample_contratos.json
```

### Executando Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/unit/test_api_client.py
pytest tests/integration/ -v

# Com cobertura
pytest --cov=src --cov-report=html

# Testes rápidos (sem integração)
pytest -m "not integration"
```

### Exemplo de Teste Unitário

```python
# tests/unit/test_api_client.py
import pytest
from unittest.mock import Mock, patch
from src.api.client import TransparenciaAPIClient

@pytest.fixture
def client():
    return TransparenciaAPIClient("test_token", "test@email.com")

def test_rate_limiter_initialization(client):
    assert client.rate_limiter.requests_per_minute == 30
    assert client.rate_limiter.tokens == 30

@patch('requests.Session.get')
def test_get_gastos_diretos_success(mock_get, client):
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {"data": [{"id": 1}]}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    # Test
    result = client.get_gastos_diretos("20000", "01", "12", "2024")
    assert "data" in result
    assert len(result["data"]) == 1
```

## 📝 Padrões de Código

### Style Guide

O projeto segue PEP 8 com algumas customizações:

```python
# Imports organizados
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union

import pandas as pd
import requests
from streamlit import components as st_components

# Constantes em UPPER_CASE
API_BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Classes com CamelCase
class DataProcessor:
    """Processa dados da API com validação e limpeza."""
    
    def __init__(self, validate_data: bool = True):
        self.validate_data = validate_data
        self.processed_count = 0
    
    def process_gastos(self, raw_data: List[Dict]) -> pd.DataFrame:
        """
        Processa dados de gastos públicos.
        
        Args:
            raw_data: Lista de dicionários com dados brutos
            
        Returns:
            DataFrame processado e validado
            
        Raises:
            ValueError: Se dados inválidos encontrados
        """
        if not raw_data:
            raise ValueError("Dados não podem estar vazios")
        
        df = pd.DataFrame(raw_data)
        return self._clean_and_validate(df)

# Funções com snake_case
def format_brazilian_currency(value: float) -> str:
    """Formata valor como moeda brasileira."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def validate_cnpj(cnpj: str) -> bool:
    """Valida CNPJ brasileiro."""
    # Implementação da validação
    pass
```

### Tratamento de Erros

```python
# Use exceções específicas
class TransparenciaAPIError(Exception):
    """Erro base para problemas da API"""
    pass

class RateLimitExceeded(TransparenciaAPIError):
    """Rate limit excedido"""
    pass

class InvalidCredentials(TransparenciaAPIError):
    """Credenciais inválidas"""
    pass

# Tratamento robusto
try:
    dados = client.get_gastos_diretos("20000", "01", "12", "2024")
except RateLimitExceeded:
    logger.warning("Rate limit excedido, aguardando...")
    time.sleep(60)
except InvalidCredentials:
    logger.error("Token inválido, verifique credenciais")
    raise
except TransparenciaAPIError as e:
    logger.error(f"Erro na API: {e}")
    # Fallback ou re-raise conforme necessário
```

### Logging

```python
import logging

# Configuração padrão
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Uso em classes
class DataCollector:
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def collect_data(self):
        self.logger.info("Iniciando coleta de dados...")
        try:
            # Lógica de coleta
            self.logger.info(f"Coletados {len(dados)} registros")
        except Exception as e:
            self.logger.error(f"Erro na coleta: {e}", exc_info=True)
            raise
```

## 🔧 Ferramentas de Desenvolvimento

### Pre-commit Hooks

```bash
# Instalar pre-commit
pip install pre-commit

# Configurar hooks
pre-commit install

# Arquivo .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.8
  
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        args: [--max-line-length=88]
  
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: [--profile=black]
```

### Formatação de Código

```bash
# Black para formatação
black src/ tests/

# isort para imports
isort src/ tests/

# flake8 para linting
flake8 src/ tests/
```

### Type Checking

```bash
# mypy para verificação de tipos
pip install mypy
mypy src/
```

## 📊 Monitoramento e Performance

### Profiling

```python
# Usar cProfile para análise de performance
import cProfile
import pstats

def profile_data_collection():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Código a ser analisado
    collector = DataCollector()
    dados = collector.collect_gastos_periodo(orgaos, inicio, fim)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Função que consome muita memória
    pass
```

### Métricas

```python
# Instrumentação básica
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} executou em {end-start:.2f}s")
        return result
    return wrapper

@timing_decorator
def expensive_operation():
    # Operação custosa
    pass
```

## 🎨 Contribuindo com o Dashboard

### Estrutura das Páginas

```python
# Template para nova página
def render_nova_pagina():
    # Header estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 30px;
                border: 1px solid #E0F2FE;">
        <h2 style="color: #047857; margin-top: 0;">🎯 Título da Página</h2>
        <p style="color: #666; font-size: 1.1em; margin-bottom: 0;">Descrição da funcionalidade</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro1 = st.selectbox("Filtro 1", opcoes1)
    
    # KPIs
    st.markdown("### 📊 Indicadores")
    col1, col2, col3, col4 = st.columns(4)
    
    # Visualizações
    tab1, tab2, tab3 = st.tabs(["Análise 1", "Análise 2", "Análise 3"])
```

### Tema Visual

```css
/* Cores padrão do projeto */
:root {
    --primary-green: #047857;
    --secondary-green: #059669;
    --light-green: #D1FAE5;
    --primary-yellow: #F59E0B;
    --light-yellow: #FEF3C7;
    --primary-blue: #1E40AF;
    --light-blue: #DBEAFE;
}
```

## 🔒 Segurança

### Boas Práticas

1. **Nunca commitar credenciais**:
```bash
# Use .env para credenciais
echo ".env" >> .gitignore
```

2. **Validação de entrada**:
```python
def validate_orgao_code(codigo: str) -> bool:
    """Valida código de órgão"""
    return codigo.isdigit() and len(codigo) == 5

def sanitize_input(user_input: str) -> str:
    """Remove caracteres perigosos"""
    import re
    return re.sub(r'[^\w\s-]', '', user_input)
```

3. **Rate limiting rigoroso**:
```python
# Sempre respeitar limites da API
if not self.rate_limiter.acquire():
    raise RateLimitExceeded("Limite de requisições excedido")
```

## 📋 Checklist para Pull Requests

- [ ] Código segue PEP 8 e padrões do projeto
- [ ] Testes unitários escritos e passando
- [ ] Testes de integração passando (se aplicável)
- [ ] Documentação atualizada
- [ ] Commit messages seguem convenção (feat:, fix:, docs:, etc.)
- [ ] Não contém credenciais ou dados sensíveis
- [ ] Performance considerada (profiling se necessário)
- [ ] Compatibilidade com Python 3.8+
- [ ] Tratamento de erros adequado
- [ ] Logging apropriado

## 🚀 Deploy e CI/CD

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 🔗 Recursos Úteis

### Documentação Externa

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [Requests Documentation](https://docs.python-requests.org/)

### Ferramentas Recomendadas

- **IDE**: VSCode com extensões Python
- **Debugging**: pdb, ipdb
- **Performance**: cProfile, memory_profiler
- **Testing**: pytest, pytest-cov
- **Formatting**: black, isort, flake8
- **Type Checking**: mypy
- **Documentation**: Sphinx (futuro)

### Templates Úteis

#### Novo Endpoint da API

```python
def get_novo_endpoint(self, param1: str, param2: str, **kwargs) -> Dict:
    """
    Descrição do novo endpoint.
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2
        **kwargs: Parâmetros adicionais
    
    Returns:
        Dados do endpoint
        
    Raises:
        TransparenciaAPIError: Erro na API
    """
    params = {
        'param1': param1,
        'param2': param2,
        **kwargs
    }
    
    return self._make_request('/novo-endpoint', params)
```

#### Nova Página do Dashboard

```python
def render_nova_pagina():
    """Renderiza nova página do dashboard"""
    # Implementar usando template padrão
    pass
```

Esta documentação será atualizada conforme o projeto evolui. Para dúvidas, abra uma issue no GitHub!