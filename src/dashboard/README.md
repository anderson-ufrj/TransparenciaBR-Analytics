# TransparenciaBR Analytics Dashboard 📊

Dashboard interativo para visualização e análise de dados do Portal da Transparência.

## 🚀 Como Executar

### Método 1: Script automatizado (Recomendado)
```bash
./run_dashboard.sh
```

### Método 2: Comando direto
```bash
streamlit run src/dashboard/app.py
```

## 📱 Funcionalidades

### Páginas Disponíveis:
1. **🏠 Início** - Visão geral com métricas principais
2. **📈 Análise de Gastos** - Visualizações detalhadas de gastos públicos
3. **🏢 Órgãos Públicos** - Dados por órgão (em desenvolvimento)
4. **📑 Contratos** - Análise de contratos (em desenvolvimento)
5. **💰 Pagamentos** - Rastreamento de pagamentos (em desenvolvimento)
6. **🏆 Licitações** - Processos licitatórios (em desenvolvimento)
7. **👥 Fornecedores** - Dados de fornecedores (em desenvolvimento)
8. **🔍 Detecção de Anomalias** - ML para detectar padrões suspeitos (em desenvolvimento)
9. **📊 Monitor de Coleta** - Status em tempo real das coletas
10. **⚙️ Configurações** - Configurações do sistema (em desenvolvimento)

## 🎨 Personalização

### Temas e Cores
O dashboard usa o tema padrão do Streamlit, mas pode ser personalizado através do arquivo `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Adicionar Nova Página
1. Crie um novo arquivo em `src/dashboard/pages/`
2. Implemente a função `render_nome_page()`
3. Adicione a importação e menu em `app.py`

## 📊 Estrutura do Código

```
dashboard/
├── app.py              # Aplicação principal
├── pages/              # Páginas do dashboard
│   ├── home.py        # Página inicial
│   ├── gastos.py      # Análise de gastos
│   └── ...
├── components/         # Componentes reutilizáveis
└── utils/             # Funções auxiliares
```

## 🔧 Desenvolvimento

### Adicionar Novos Gráficos
```python
import plotly.express as px

# Exemplo de gráfico
fig = px.bar(df, x='categoria', y='valor', title='Gastos por Categoria')
st.plotly_chart(fig, use_container_width=True)
```

### Conectar com Dados Reais
```python
from src.data.processor import DataProcessor

# Carregar dados processados
processor = DataProcessor()
df = processor.load_processed_data('contratos')
```

## 🐛 Solução de Problemas

### Dashboard não inicia
- Verifique se as dependências estão instaladas: `pip install -r requirements.txt`
- Confirme que está no diretório correto
- Verifique se a porta 8501 está disponível

### Erro de importação
- Certifique-se de executar do diretório raiz do projeto
- Verifique se o arquivo `.env` existe

### Dados não aparecem
- Execute a coleta de dados primeiro: `python -m src.data.collector`
- Verifique as credenciais da API no arquivo `.env`

## 📈 Próximas Melhorias

- [ ] Implementar todas as páginas pendentes
- [ ] Adicionar filtros avançados
- [ ] Criar componentes reutilizáveis
- [ ] Implementar cache para melhor performance
- [ ] Adicionar export de relatórios
- [ ] Criar modo dark/light
- [ ] Adicionar autenticação de usuários