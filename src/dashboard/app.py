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

# CSS para esconder a navegação de páginas padrão do Streamlit
st.markdown("""
<style>
    /* Esconder navegação de páginas padrão */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Remover padding extra do sidebar */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Esconder o header padrão de páginas */
    .css-1avcm0n {
        display: none;
    }
    
    .css-18e3th9 {
        padding-top: 0;
    }
</style>
""", unsafe_allow_html=True)

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
    
    # Menu de navegação customizado
    st.markdown("""
    <style>
        /* Estilo do menu customizado */
        .menu-title {
            color: #047857;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 20px;
            padding: 10px;
            background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
            border-radius: 12px;
            text-align: center;
            border: 2px solid #D1FAE5;
        }
        
        .menu-item {
            background: #FFFFFF;
            border: 2px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: #374151;
        }
        
        .menu-item:hover {
            background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
            border-color: #047857;
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(4, 120, 87, 0.2);
        }
        
        .menu-item.active {
            background: linear-gradient(135deg, #047857 0%, #059669 100%);
            color: white;
            border-color: #047857;
            box-shadow: 0 4px 16px rgba(4, 120, 87, 0.3);
        }
        
        .menu-icon {
            font-size: 1.5rem;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #F3F4F6;
            border-radius: 10px;
        }
        
        .menu-item.active .menu-icon {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .menu-text {
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        .menu-description {
            font-size: 0.75rem;
            opacity: 0.7;
            margin-top: 2px;
        }
        
        .menu-section {
            margin-bottom: 30px;
        }
        
        .menu-section-title {
            color: #6B7280;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 20px 0 12px 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="menu-title">📊 Painel de Navegação</div>', unsafe_allow_html=True)
    
    # Menu items com descrições
    menu_options = {
        "🏠 Início": {
            "key": "home",
            "desc": "Visão geral e métricas",
            "section": "principal"
        },
        "📈 Análise de Gastos": {
            "key": "gastos",
            "desc": "Gastos por categoria e período",
            "section": "principal"
        },
        "🏢 Órgãos Públicos": {
            "key": "orgaos",
            "desc": "Rankings e comparações",
            "section": "principal"
        },
        "📑 Contratos": {
            "key": "contratos",
            "desc": "Gestão e análise de contratos",
            "section": "gestao"
        },
        "💰 Pagamentos": {
            "key": "pagamentos",
            "desc": "Fluxo de pagamentos",
            "section": "gestao"
        },
        "🏆 Licitações": {
            "key": "licitacoes",
            "desc": "Processos licitatórios",
            "section": "gestao"
        },
        "👥 Fornecedores": {
            "key": "fornecedores",
            "desc": "Análise de fornecedores",
            "section": "gestao"
        },
        "🔍 Detecção de Anomalias": {
            "key": "anomalias",
            "desc": "Machine Learning e alertas",
            "section": "avancado"
        },
        "📊 Monitor de Coleta": {
            "key": "monitor",
            "desc": "Status do sistema",
            "section": "avancado"
        },
        "⚙️ Configurações": {
            "key": "configuracoes",
            "desc": "Preferências e API",
            "section": "avancado"
        }
    }
    
    # Agrupar por seções
    sections = {
        "principal": "Dashboard Principal",
        "gestao": "Gestão e Controle",
        "avancado": "Recursos Avançados"
    }
    
    # Inicializar página no session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Início"
    
    # Renderizar menu por seções
    for section_key, section_title in sections.items():
        st.markdown(f'<div class="menu-section-title">{section_title}</div>', unsafe_allow_html=True)
        
        for option, details in menu_options.items():
            if details["section"] == section_key:
                # Estilo do botão baseado na página ativa
                button_type = "primary" if st.session_state.current_page == option else "secondary"
                
                if st.button(
                    option,
                    key=details["key"],
                    use_container_width=True,
                    help=details["desc"],
                    type=button_type
                ):
                    st.session_state.current_page = option
                    st.rerun()
    
    page = st.session_state.current_page
    
    st.markdown("---")
    
    # Estatísticas visuais
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%); 
                padding: 20px; 
                border-radius: 12px; 
                border: 2px solid #D1FAE5;
                margin-bottom: 20px;">
        <h4 style="color: #047857; margin: 0 0 15px 0; font-size: 1.1rem;">📊 Estatísticas Rápidas</h4>
        <div style="display: grid; gap: 10px;">
            <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #E5E7EB;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #6B7280; font-size: 0.85rem;">Contratos Ativos</span>
                    <span style="color: #047857; font-weight: 700; font-size: 1.2rem;">782</span>
                </div>
                <div style="background: #E5E7EB; height: 4px; border-radius: 2px; margin-top: 8px;">
                    <div style="background: #047857; height: 100%; width: 78%; border-radius: 2px;"></div>
                </div>
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #E5E7EB;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #6B7280; font-size: 0.85rem;">Taxa de Análise</span>
                    <span style="color: #F59E0B; font-weight: 700; font-size: 1.2rem;">94%</span>
                </div>
                <div style="background: #E5E7EB; height: 4px; border-radius: 2px; margin-top: 8px;">
                    <div style="background: #F59E0B; height: 100%; width: 94%; border-radius: 2px;"></div>
                </div>
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #E5E7EB;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #6B7280; font-size: 0.85rem;">Alertas Hoje</span>
                    <span style="color: #EF4444; font-weight: 700; font-size: 1.2rem;">23</span>
                </div>
                <div style="background: #E5E7EB; height: 4px; border-radius: 2px; margin-top: 8px;">
                    <div style="background: #EF4444; height: 100%; width: 23%; border-radius: 2px;"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Links úteis com design melhorado
    st.markdown("""
    <div style="background: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
        <h4 style="color: #374151; margin: 0 0 15px 0; font-size: 1rem;">🔗 Links Rápidos</h4>
        <div style="display: grid; gap: 10px;">
            <a href="https://github.com/anderson-ufrj/TransparenciaBR-Analytics" target="_blank" 
               style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #E5E7EB;
                      text-decoration: none; color: #374151; display: flex; align-items: center; gap: 10px;
                      transition: all 0.2s; cursor: pointer;"
               onmouseover="this.style.borderColor='#047857'; this.style.transform='translateX(2px)'"
               onmouseout="this.style.borderColor='#E5E7EB'; this.style.transform='translateX(0)'">
                <span style="font-size: 1.2rem;">💻</span>
                <div>
                    <div style="font-weight: 600; font-size: 0.9rem;">Código Fonte</div>
                    <div style="font-size: 0.75rem; color: #6B7280;">GitHub Repository</div>
                </div>
            </a>
            <a href="https://api.portaldatransparencia.gov.br/" target="_blank"
               style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #E5E7EB;
                      text-decoration: none; color: #374151; display: flex; align-items: center; gap: 10px;
                      transition: all 0.2s; cursor: pointer;"
               onmouseover="this.style.borderColor='#047857'; this.style.transform='translateX(2px)'"
               onmouseout="this.style.borderColor='#E5E7EB'; this.style.transform='translateX(0)'">
                <span style="font-size: 1.2rem;">🌐</span>
                <div>
                    <div style="font-weight: 600; font-size: 0.9rem;">Portal da Transparência</div>
                    <div style="font-size: 0.75rem; color: #6B7280;">Fonte de Dados</div>
                </div>
            </a>
            <a href="https://anderson-ufrj.github.io/TransparenciaBR-Analytics/" target="_blank"
               style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #E5E7EB;
                      text-decoration: none; color: #374151; display: flex; align-items: center; gap: 10px;
                      transition: all 0.2s; cursor: pointer;"
               onmouseover="this.style.borderColor='#047857'; this.style.transform='translateX(2px)'"
               onmouseout="this.style.borderColor='#E5E7EB'; this.style.transform='translateX(0)'">
                <span style="font-size: 1.2rem;">📚</span>
                <div>
                    <div style="font-weight: 600; font-size: 0.9rem;">Documentação</div>
                    <div style="font-size: 0.75rem; color: #6B7280;">Guias e Tutoriais</div>
                </div>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer do sidebar
    st.markdown("""
    <div style="margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #064E3B 0%, #047857 100%); 
                border-radius: 12px; text-align: center;">
        <div style="color: white; font-size: 0.8rem; opacity: 0.9;">
            Desenvolvido por
        </div>
        <a href="https://www.linkedin.com/in/anderson-h-silva95/" target="_blank"
           style="color: white; font-weight: 700; text-decoration: none; font-size: 0.95rem;">
            Anderson H. Silva
        </a>
        <div style="color: white; font-size: 0.75rem; margin-top: 8px; opacity: 0.8;">
            © 2025 - Licença Proprietária
        </div>
    </div>
    """, unsafe_allow_html=True)

# Conteúdo principal baseado na página selecionada
if page == "🏠 Início":
    # Importar página inicial
    from src.dashboard.pages.home import render_home_page
    render_home_page()

elif page == "📈 Análise de Gastos":
    from src.dashboard.pages.gastos import render_gastos_page
    render_gastos_page()

elif page == "🏢 Órgãos Públicos":
    from src.dashboard.pages.orgaos import render_orgaos_page
    render_orgaos_page()

elif page == "📑 Contratos":
    from src.dashboard.pages.contratos import render_contratos_page
    render_contratos_page()

elif page == "💰 Pagamentos":
    from src.dashboard.pages.pagamentos import render_pagamentos_page
    render_pagamentos_page()

elif page == "🏆 Licitações":
    from src.dashboard.pages.licitacoes import render_licitacoes_page
    render_licitacoes_page()

elif page == "👥 Fornecedores":
    from src.dashboard.pages.fornecedores import render_fornecedores_page
    render_fornecedores_page()

elif page == "🔍 Detecção de Anomalias":
    from src.dashboard.pages.anomalias import render_anomalias_page
    render_anomalias_page()

elif page == "📊 Monitor de Coleta":
    from src.dashboard.pages.monitor import render_monitor_page
    render_monitor_page()

elif page == "⚙️ Configurações":
    from src.dashboard.pages.configuracoes import render_configuracoes_page
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