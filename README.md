# TransparenciaBR-Analytics 🇧🇷

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![API](https://img.shields.io/badge/API-Portal%20da%20Transparência-orange.svg)](https://api.portaldatransparencia.gov.br/)

Uma plataforma completa para análise de dados do Portal da Transparência do Governo Federal Brasileiro, com foco em Machine Learning e visualizações interativas.

## 🎯 Objetivos

- **Coletar e processar** dados públicos do Portal da Transparência
- **Analisar padrões** em gastos públicos, contratos e licitações
- **Detectar anomalias** usando técnicas de Machine Learning
- **Visualizar insights** através de dashboards interativos
- **Democratizar o acesso** à informação pública

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8 ou superior
- Git
- Conta e chave de API do [Portal da Transparência](https://api.portaldatransparencia.gov.br/)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/anderson-ufrj/TransparenciaBR-Analytics.git
cd TransparenciaBR-Analytics
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.template .env
# Edite o arquivo .env com suas credenciais
```

5. Valide a instalação:
```bash
python scripts/validate_setup.py
```

## 📊 Estrutura do Projeto

```
TransparenciaBR-Analytics/
├── data/                    # Dados coletados e processados
│   ├── raw/                # Dados brutos da API
│   ├── processed/          # Dados processados
│   └── cache/              # Cache de requisições
├── notebooks/              # Notebooks Jupyter para análise
│   ├── 00_setup_validation.ipynb
│   ├── 01_exploratory/     # Análises exploratórias
│   └── 02_analysis/        # Análises avançadas
├── src/                    # Código fonte principal
│   ├── api/               # Cliente da API
│   ├── data/              # Pipeline de dados
│   ├── models/            # Modelos de ML
│   ├── dashboard/         # Dashboard Streamlit
│   └── utils/             # Funções auxiliares
├── tests/                  # Testes automatizados
├── scripts/                # Scripts utilitários
├── docs/                   # Documentação
└── reports/                # Relatórios gerados
```

## 🔧 Uso Básico

### 1. Exploração da API

```python
from src.api.client import TransparenciaAPIClient

# Inicializar cliente
client = TransparenciaAPIClient()

# Buscar contratos
contratos = client.get_contratos(pagina=1, quantidade=100)

# Buscar pagamentos
pagamentos = client.get_pagamentos(ano=2024)
```

### 2. Coleta de Dados

```python
from src.data.collector import DataCollector

# Coletar dados de múltiplos endpoints
collector = DataCollector()
results = collector.collect_all(
    endpoints=["contratos", "pagamentos", "licitacoes"],
    incremental=True
)
```

### 3. Processamento de Dados

```python
from src.data.processor import DataProcessor

# Processar dados coletados
processor = DataProcessor()
df_processed = processor.process_dataset("contratos")
```

### 4. Executar Dashboard

```bash
streamlit run src/dashboard/app.py
```

## 📈 Funcionalidades

### API Client
- ✅ Rate limiting automático (30 req/min)
- ✅ Sistema de retry com backoff exponencial
- ✅ Cache inteligente com TTL configurável
- ✅ Suporte a todos os endpoints principais
- ✅ Paginação automática

### Pipeline de Dados
- ✅ Coleta incremental de dados
- ✅ Processamento e limpeza automatizados
- ✅ Armazenamento eficiente em Parquet
- ✅ Validação de qualidade de dados
- ✅ Feature engineering

### Análises
- 📊 Análise exploratória de dados
- 🔍 Detecção de anomalias
- 📈 Previsão de gastos
- 🗺️ Visualizações geográficas
- 📱 Dashboard interativo

## 🧪 Testes

Execute os testes com:

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Apenas testes de API
pytest tests/test_api_connection.py -v
```

## 📚 Documentação

- [Guia da API](docs/API_GUIDE.md)
- [Dicionário de Dados](docs/DATA_DICTIONARY.md)
- [Contribuindo](docs/CONTRIBUTING.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📊 Exemplos de Uso

### Análise de Contratos por Órgão

```python
import pandas as pd
from src.api.client import TransparenciaAPIClient

client = TransparenciaAPIClient()

# Coletar contratos
contratos = client.paginate(
    client.get_contratos,
    max_pages=10,
    ano=2024
)

# Analisar por órgão
df = pd.DataFrame(contratos)
analise = df.groupby('nomeOrgao')['valorInicial'].agg(['sum', 'count', 'mean'])
print(analise.sort_values('sum', ascending=False).head(10))
```

### Detecção de Anomalias em Pagamentos

```python
from src.models.anomaly_detector import AnomalyDetector

detector = AnomalyDetector()
anomalias = detector.detect_payment_anomalies(df_pagamentos)
```

## 🗺️ Roadmap

- [x] Cliente API com rate limiting
- [x] Pipeline de coleta de dados
- [x] Notebooks de análise exploratória
- [ ] Modelos de detecção de anomalias
- [ ] Dashboard interativo completo
- [ ] API REST própria
- [ ] Análises preditivas
- [ ] Integração com outras fontes de dados

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Portal da Transparência](https://www.portaldatransparencia.gov.br/) pela disponibilização dos dados
- Comunidade open source pelos pacotes utilizados

## 📧 Contato

Anderson Henrique - [@anderson-ufrj](https://github.com/anderson-ufrj)

Link do Projeto: [https://github.com/anderson-ufrj/TransparenciaBR-Analytics](https://github.com/anderson-ufrj/TransparenciaBR-Analytics)

---

🇧🇷 Feito com ❤️ para aumentar a transparência pública no Brasil