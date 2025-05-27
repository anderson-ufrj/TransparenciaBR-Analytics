"""
TransparenciaBR Analytics Dashboard
Dashboard interativo para análise de dados do Portal da Transparência
"""

import streamlit as st
import sys
from pathlib import Path
import base64

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

# CSS customizado com tema Brasil
st.markdown("""
<style>
    /* Importar fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Tema geral */
    .main {
        padding-top: 2rem;
        background-color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar estilizada */
    .css-1d391kg {
        background-color: #F8FAFC;
        border-right: 3px solid #D1D5DB;
    }
    
    /* Métricas com cores do Brasil */
    div[data-testid="metric-container"] {
        background: #FFFFFF;
        border: 2px solid #D1D5DB;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
        border-color: #047857;
    }
    
    /* Títulos verdes */
    h1, h2, h3 {
        color: #064E3B;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Botões estilo Brasil */
    .stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065F46 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }
    
    /* Cards informativos */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #E5E7EB;
        margin-bottom: 20px;
    }
    
    /* Header com gradiente brasileiro */
    .brazil-bg {
        background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 50%, #F0F9FF 100%);
        border: 2px solid #D1FAE5;
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(4, 120, 87, 0.1);
    }
    
    /* Alertas customizados */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F3F4F6;
        padding: 4px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Selectbox estilizado */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    
    /* DataFrame estilizado */
    .dataframe {
        border: none !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Links verdes */
    a {
        color: #059669;
        text-decoration: none;
    }
    
    a:hover {
        color: #047857;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Header com bandeira do Brasil
# Carregar bandeira do Brasil local
flag_path = Path(__file__).parent.parent / "images" / "bandeira-brasil.png"
if flag_path.exists():
    with open(flag_path, "rb") as f:
        flag_data = base64.b64encode(f.read()).decode()
    flag_src = f"data:image/png;base64,{flag_data}"
else:
    flag_src = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/640px-Flag_of_Brazil.svg.png"

st.markdown(f"""
<div class="brazil-bg">
    <div style="display: flex; align-items: center; gap: 24px;">
        <img src="{flag_src}" 
             width="120" style="border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); border: 2px solid #FFFFFF;">
        <div>
            <h1 style="margin: 0; color: #064E3B; font-size: 2.8rem; font-weight: 800; letter-spacing: -0.02em;">
                TransparenciaBR Analytics
            </h1>
            <p style="margin: 8px 0 0 0; color: #047857; font-size: 1.3rem; font-weight: 600;">
                Análise inteligente de dados públicos do Portal da Transparência
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Barra lateral
with st.sidebar:
    # Imagem de Brasília
    # Carregar imagem local
    img_path = Path(__file__).parent.parent / "images" / "brasilia.jpg"
    if img_path.exists():
        with open(img_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        img_src = f"data:image/jpeg;base64,{img_data}"
    else:
        # Fallback para URL online
        img_src = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Congresso_Nacional_Brasil_Brasilia.jpg/640px-Congresso_Nacional_Brasil_Brasilia.jpg"
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 24px; padding: 12px; background: #F8FAFC; border-radius: 16px; border: 1px solid #E5E7EB;">
        <img src="{img_src}" 
             width="100%" style="border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.15);">
        <p style="margin-top: 12px; color: #374151; font-size: 0.875rem; font-weight: 600;">
            🏛️ Congresso Nacional - Brasília
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
st.markdown("""
<div style="background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); padding: 30px; border-radius: 16px; margin-top: 50px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Coat_of_arms_of_Brazil.svg/180px-Coat_of_arms_of_Brazil.svg.png" 
                 width="50" style="opacity: 0.8;">
            <div>
                <p style="margin: 0; font-weight: 600; color: #047857;">TransparenciaBR Analytics</p>
                <p style="margin: 0; font-size: 0.875rem; color: #6B7280;">Transparência e Dados Abertos</p>
            </div>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; font-size: 0.875rem; color: #6B7280;">Desenvolvido por Anderson Henrique</p>
            <p style="margin: 0; font-size: 0.875rem; color: #6B7280;">Dados: Portal da Transparência • v0.1.0</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)