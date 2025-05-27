# 📡 Documentação da API

Este documento descreve como usar o cliente da API do Portal da Transparência implementado no projeto.

## 🏗️ Arquitetura

O cliente da API é composto por três componentes principais:

- **TransparenciaAPIClient**: Cliente principal para acessar a API
- **RateLimiter**: Controlador de taxa de requisições
- **CacheManager**: Sistema de cache com TTL

## 🚀 Início Rápido

### Configuração Básica

```python
from src.api.client import TransparenciaAPIClient
import os

# Configurar credenciais
api_token = os.getenv('TRANSPARENCIA_API_TOKEN')
email = os.getenv('TRANSPARENCIA_EMAIL')

# Criar cliente
client = TransparenciaAPIClient(api_token=api_token, email=email)
```

### Exemplo de Uso

```python
# Buscar gastos diretos
gastos = client.get_gastos_diretos(
    codigo_orgao='20000',
    mes_inicial='01',
    mes_final='12',
    ano='2024'
)

# Buscar cartões de pagamento
cartoes = client.get_cartao_pagamento(
    mes='01',
    ano='2024',
    cpf='***.123.456-**'
)

# Buscar contratos
contratos = client.get_contratos(
    codigo_orgao='20000',
    data_inicial='01/01/2024',
    data_final='31/12/2024'
)
```

## 📚 Referência da API

### 💰 Gastos Diretos

#### `get_gastos_diretos(codigo_orgao, mes_inicial, mes_final, ano, **kwargs)`

Recupera dados de gastos diretos do governo.

**Parâmetros:**
- `codigo_orgao` (str): Código do órgão público
- `mes_inicial` (str): Mês inicial (formato: '01'-'12')
- `mes_final` (str): Mês final (formato: '01'-'12')
- `ano` (str): Ano de referência
- `codigo_favorecido` (str, optional): CNPJ/CPF do favorecido
- `pagina` (int, optional): Número da página (padrão: 1)

**Retorno:**
```python
{
    "data": [
        {
            "dataDocumento": "2024-01-15",
            "nomeOrgao": "Ministério da Saúde",
            "valorDocumento": 150000.50,
            "nomeFavorecido": "Empresa XYZ Ltda",
            "numeroDocumento": "2024NE000123"
        }
    ],
    "links": {...},
    "pagina": 1,
    "totalPaginas": 10
}
```

### 💳 Cartão de Pagamento

#### `get_cartao_pagamento(mes, ano, cpf, **kwargs)`

Recupera dados de gastos com cartão de pagamento corporativo.

**Parâmetros:**
- `mes` (str): Mês de referência
- `ano` (str): Ano de referência
- `cpf` (str): CPF do portador (pode usar máscara)
- `codigo_orgao` (str, optional): Código do órgão

**Retorno:**
```python
{
    "data": [
        {
            "nomePortador": "João da Silva",
            "valorTransacao": 1250.75,
            "dataTransacao": "2024-01-15",
            "estabelecimento": "Hotel ABC",
            "cnpjEstabelecimento": "12.345.678/0001-00"
        }
    ]
}
```

### 📑 Contratos

#### `get_contratos(codigo_orgao, data_inicial, data_final, **kwargs)`

Recupera informações sobre contratos públicos.

**Parâmetros:**
- `codigo_orgao` (str): Código do órgão
- `data_inicial` (str): Data inicial (DD/MM/AAAA)
- `data_final` (str): Data final (DD/MM/AAAA)
- `cnpj_contratada` (str, optional): CNPJ da empresa contratada

**Retorno:**
```python
{
    "data": [
        {
            "numeroContrato": "CT-2024-001",
            "nomeRazaoSocialFornecedor": "Tech Solutions Ltda",
            "valorInicialContrato": 2500000.00,
            "dataInicioVigencia": "2024-01-01",
            "dataFimVigencia": "2024-12-31",
            "objetoContrato": "Serviços de desenvolvimento de software"
        }
    ]
}
```

### 👥 Fornecedores

#### `get_fornecedores(**kwargs)`

Lista fornecedores cadastrados no sistema.

**Parâmetros:**
- `cnpj_cpf` (str, optional): CNPJ/CPF do fornecedor
- `nome` (str, optional): Nome/razão social
- `pagina` (int, optional): Página de resultados

### 🏆 Licitações

#### `get_licitacoes(codigo_orgao, data_inicial, data_final, **kwargs)`

Recupera dados de licitações públicas.

**Parâmetros:**
- `codigo_orgao` (str): Código do órgão
- `data_inicial` (str): Data inicial
- `data_final` (str): Data final
- `modalidade` (str, optional): Modalidade da licitação

### 🏢 Órgãos

#### `get_orgaos(**kwargs)`

Lista órgãos públicos cadastrados.

**Parâmetros:**
- `codigo_orgao` (str, optional): Código específico
- `nome` (str, optional): Nome do órgão

### 🚀 Viagens

#### `get_viagens(codigo_orgao, ano, **kwargs)`

Recupera dados de viagens oficiais.

**Parâmetros:**
- `codigo_orgao` (str): Código do órgão
- `ano` (str): Ano de referência
- `cpf_viajante` (str, optional): CPF do viajante

## ⚙️ Configurações Avançadas

### Rate Limiting

O cliente implementa rate limiting automático para respeitar os limites da API:

```python
# Configurar limite personalizado (padrão: 30 req/min)
client = TransparenciaAPIClient(
    api_token=token,
    email=email,
    requests_per_minute=20  # Limite customizado
)
```

### Cache

Sistema de cache automático para reduzir requisições:

```python
# Cache é habilitado por padrão
# TTL padrão: 1 hora para a maioria dos endpoints
# TTL para dados dinâmicos: 5 minutos

# Limpar cache manualmente
client.cache_manager.clear_cache()

# Desabilitar cache
client.cache_manager.enabled = False
```

### Retry Logic

Retry automático com backoff exponencial:

```python
# Configuração padrão:
# - 3 tentativas máximas
# - Backoff inicial: 1 segundo
# - Multiplicador: 2
# - Jitter aleatório para evitar thundering herd

# Customizar configuração de retry
client.session.mount('https://', HTTPAdapter(
    max_retries=Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504]
    )
))
```

## 🔒 Segurança

### Autenticação

A API requer token de acesso e email:

```python
# Usar variáveis de ambiente (recomendado)
TRANSPARENCIA_API_TOKEN=seu_token_aqui
TRANSPARENCIA_EMAIL=seu_email@exemplo.com

# Evitar hardcoding de credenciais no código
client = TransparenciaAPIClient(
    api_token=os.getenv('TRANSPARENCIA_API_TOKEN'),
    email=os.getenv('TRANSPARENCIA_EMAIL')
)
```

### Headers de Segurança

O cliente adiciona automaticamente headers necessários:

```python
{
    'chave-api-dados': 'seu_token',
    'User-Agent': 'TransparenciaBR-Analytics/1.0',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
```

## 🐛 Tratamento de Erros

### Tipos de Erro

```python
from src.api.client import TransparenciaAPIClient
from requests.exceptions import HTTPError, Timeout, RequestException

try:
    dados = client.get_gastos_diretos('20000', '01', '12', '2024')
except HTTPError as e:
    if e.response.status_code == 401:
        print("Token inválido ou expirado")
    elif e.response.status_code == 429:
        print("Limite de rate exceeded")
    elif e.response.status_code == 500:
        print("Erro interno do servidor")
except Timeout:
    print("Timeout na requisição")
except RequestException as e:
    print(f"Erro de rede: {e}")
```

### Logs

O cliente registra automaticamente:

```python
import logging

# Configurar nível de log
logging.getLogger('transparencia_client').setLevel(logging.DEBUG)

# Logs incluem:
# - Requisições feitas
# - Rate limiting aplicado
# - Cache hits/misses
# - Erros e retries
```

## 📊 Monitoramento

### Métricas

```python
# Acessar estatísticas do cliente
stats = client.get_stats()
print(f"Requisições feitas: {stats['total_requests']}")
print(f"Cache hits: {stats['cache_hits']}")
print(f"Rate limits aplicados: {stats['rate_limited']}")
```

### Health Check

```python
# Verificar conectividade
if client.health_check():
    print("API está acessível")
else:
    print("Problemas de conectividade")
```

## 🔄 Paginação

Para endpoints com muitos resultados:

```python
def obter_todos_gastos(client, codigo_orgao, ano):
    """Exemplo de paginação automática"""
    todos_dados = []
    pagina = 1
    
    while True:
        resultado = client.get_gastos_diretos(
            codigo_orgao=codigo_orgao,
            mes_inicial='01',
            mes_final='12',
            ano=ano,
            pagina=pagina
        )
        
        todos_dados.extend(resultado['data'])
        
        if pagina >= resultado.get('totalPaginas', 1):
            break
            
        pagina += 1
    
    return todos_dados
```

## 🚨 Limites e Quotas

### Limites da API

- **Rate Limit**: 30 requisições por minuto
- **Timeout**: 30 segundos por requisição
- **Tamanho máximo**: 1000 registros por página
- **Período de dados**: A partir de 2013

### Boas Práticas

1. **Use cache**: Ative o cache para dados que não mudam frequentemente
2. **Paginação eficiente**: Processe dados em lotes para evitar timeouts
3. **Retry inteligente**: Implemente retry com backoff exponencial
4. **Monitoramento**: Acompanhe métricas de uso da API
5. **Filtros específicos**: Use filtros para reduzir volume de dados

## 🔗 Links Úteis

- [Portal da Transparência](https://www.portaldatransparencia.gov.br/)
- [Documentação Oficial da API](https://api.portaldatransparencia.gov.br/)
- [Solicitar Token de Acesso](https://api.portaldatransparencia.gov.br/)
- [Status da API](https://status.portaldatransparencia.gov.br/)

## 📈 Exemplos Avançados

### Análise de Gastos por Período

```python
from datetime import datetime, timedelta
import pandas as pd

def analisar_gastos_periodo(client, codigo_orgao, meses=12):
    """Analisa gastos dos últimos N meses"""
    dados = []
    hoje = datetime.now()
    
    for i in range(meses):
        data = hoje - timedelta(days=30 * i)
        mes = f"{data.month:02d}"
        ano = str(data.year)
        
        gastos = client.get_gastos_diretos(
            codigo_orgao=codigo_orgao,
            mes_inicial=mes,
            mes_final=mes,
            ano=ano
        )
        
        dados.extend(gastos['data'])
    
    return pd.DataFrame(dados)
```

### Monitoramento de Contratos

```python
def monitorar_contratos_vencimento(client, dias_antecedencia=30):
    """Monitora contratos próximos ao vencimento"""
    hoje = datetime.now()
    limite = hoje + timedelta(days=dias_antecedencia)
    
    # Buscar contratos de todos os órgãos principais
    orgaos = ['20000', '26000', '30000']  # Exemplo
    contratos_vencendo = []
    
    for orgao in orgaos:
        contratos = client.get_contratos(
            codigo_orgao=orgao,
            data_inicial=hoje.strftime('%d/%m/%Y'),
            data_final=limite.strftime('%d/%m/%Y')
        )
        
        for contrato in contratos['data']:
            data_fim = datetime.strptime(
                contrato['dataFimVigencia'], 
                '%Y-%m-%d'
            )
            
            if data_fim <= limite:
                contratos_vencendo.append(contrato)
    
    return contratos_vencendo
```