"""
TransparenciaBR Analytics Dashboard
Dashboard interativo para análise de dados do Portal da Transparência
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configuração da página
st.set_page_config(
    page_title="TransparenciaBR Analytics",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/anderson-ufrj/TransparenciaBR-Analytics',
        'Report a bug': "https://github.com/anderson-ufrj/TransparenciaBR-Analytics/issues",
        'About': "# TransparenciaBR Analytics\nAnálise de dados públicos do Portal da Transparência"
    }
)

# CSS customizado
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(28, 131, 225, 0.1);
        border: 1px solid rgba(28, 131, 225, 0.1);
        padding: 5% 5% 5% 10%;
        border-radius: 5px;
        color: rgb(30, 103, 119);
        overflow-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

# Header com logo e título
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("# 🇧🇷")
with col2:
    st.title("TransparenciaBR Analytics")
    st.markdown("**Análise inteligente de dados públicos do Portal da Transparência**")

# Barra lateral
with st.sidebar:
    st.markdown("## 📊 Navegação")
    
    # Menu de navegação
    page = st.selectbox(
        "Selecione uma página",
        [
            "🏠 Início",
            "📈 Análise de Gastos",
            "🏢 Órgãos Públicos",
            "📑 Contratos",
            "💰 Pagamentos",
            "🏆 Licitações",
            "👥 Fornecedores",
            "🔍 Detecção de Anomalias",
            "📊 Monitor de Coleta",
            "⚙️ Configurações"
        ]
    )
    
    st.markdown("---")
    
    # Informações do sistema
    st.markdown("### 💡 Status do Sistema")
    
    # Verificar conexão com API
    try:
        from src.api.client import TransparenciaAPIClient
        client = TransparenciaAPIClient()
        
        if client.test_connection():
            st.success("✅ API Conectada")
        else:
            st.error("❌ API Desconectada")
    except Exception as e:
        st.error("❌ Erro na API")
        st.caption(str(e)[:50] + "...")
    
    # Verificar dados disponíveis
    data_dir = Path("data/raw")
    if data_dir.exists():
        total_files = sum(1 for _ in data_dir.rglob("*.parquet"))
        st.info(f"📁 {total_files} arquivos de dados")
    else:
        st.warning("📁 Sem dados coletados")
    
    st.markdown("---")
    
    # Links úteis
    st.markdown("### 🔗 Links Úteis")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/anderson-ufrj/TransparenciaBR-Analytics)")
    st.markdown("[![API](https://img.shields.io/badge/API-Portal%20da%20Transparência-blue)](https://api.portaldatransparencia.gov.br/)")

# Conteúdo principal baseado na página selecionada
if page == "🏠 Início":
    # Importar página inicial
    from pages.home import render_home_page
    render_home_page()

elif page == "📈 Análise de Gastos":
    from pages.gastos import render_gastos_page
    render_gastos_page()

elif page == "🏢 Órgãos Públicos":
    from pages.orgaos import render_orgaos_page
    render_orgaos_page()

elif page == "📑 Contratos":
    from pages.contratos import render_contratos_page
    render_contratos_page()

elif page == "💰 Pagamentos":
    from pages.pagamentos import render_pagamentos_page
    render_pagamentos_page()

elif page == "🏆 Licitações":
    from pages.licitacoes import render_licitacoes_page
    render_licitacoes_page()

elif page == "👥 Fornecedores":
    from pages.fornecedores import render_fornecedores_page
    render_fornecedores_page()

elif page == "🔍 Detecção de Anomalias":
    from pages.anomalias import render_anomalias_page
    render_anomalias_page()

elif page == "📊 Monitor de Coleta":
    from pages.monitor import render_monitor_page
    render_monitor_page()

elif page == "⚙️ Configurações":
    from pages.configuracoes import render_configuracoes_page
    render_configuracoes_page()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("Desenvolvido por Anderson Henrique")
with col2:
    st.caption("Dados: Portal da Transparência")
with col3:
    st.caption("v0.1.0 - 2025")