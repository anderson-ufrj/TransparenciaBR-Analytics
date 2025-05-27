"""Página de configurações."""
import streamlit as st
import pandas as pd
from datetime import datetime
import json

def render_configuracoes_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #E0E7FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                margin-bottom: 30px;">
        <h2 style="color: #4C1D95; margin: 0; font-size: 32px;">
            ⚙️ Configurações
        </h2>
        <p style="color: #6B7280; margin-top: 10px; margin-bottom: 0;">
            Personalize sua experiência e gerencie preferências do sistema
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs de configuração
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎨 Aparência", 
        "🔔 Notificações",
        "📊 Dados e API",
        "👤 Perfil",
        "🔒 Segurança"
    ])
    
    with tab1:
        st.subheader("Personalização da Interface")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎨 Tema")
            tema = st.selectbox(
                "Escolha o tema do dashboard",
                ["🌞 Claro", "🌙 Escuro", "🤖 Automático (Sistema)"],
                index=0
            )
            
            st.markdown("### 🎯 Layout")
            layout = st.radio(
                "Densidade de informação",
                ["Compacto", "Normal", "Espaçoso"],
                index=1
            )
            
            st.markdown("### 🗣️ Idioma")
            idioma = st.selectbox(
                "Idioma da interface",
                ["🇧🇷 Português (Brasil)", "🇺🇸 English", "🇪🇸 Español"],
                index=0
            )
        
        with col2:
            st.markdown("### 📊 Gráficos")
            
            animacoes = st.checkbox("Ativar animações nos gráficos", value=True)
            tooltips = st.checkbox("Mostrar dicas flutuantes", value=True)
            grid = st.checkbox("Exibir grade nos gráficos", value=False)
            
            st.markdown("### 🎨 Paleta de Cores")
            paleta = st.selectbox(
                "Esquema de cores dos gráficos",
                ["Verde e Amarelo", "Azul e Cinza", "Multicolorido", "Monocromático"],
                index=0
            )
            
            # Preview
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; 
                        border: 1px solid #E5E7EB; margin-top: 20px;">
                <h4 style="color: #374151; margin-bottom: 10px;">👁️ Preview</h4>
                <p style="color: #6B7280; margin: 0;">
                    As alterações serão aplicadas após salvar as configurações.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Preferências de Notificação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📧 Notificações por Email")
            
            email_ativo = st.checkbox("Receber notificações por email", value=True)
            
            if email_ativo:
                email = st.text_input("Email para notificações", value="usuario@example.com")
                
                st.markdown("#### Tipos de Notificação")
                notif_anomalias = st.checkbox("Anomalias detectadas", value=True)
                notif_relatorios = st.checkbox("Relatórios semanais", value=True)
                notif_atualizacoes = st.checkbox("Atualizações do sistema", value=False)
                notif_alertas = st.checkbox("Alertas críticos", value=True)
        
        with col2:
            st.markdown("### 🔔 Notificações no Dashboard")
            
            push_ativo = st.checkbox("Notificações em tempo real", value=True)
            
            if push_ativo:
                st.markdown("#### Frequência")
                frequencia = st.radio(
                    "Quando mostrar notificações",
                    ["Imediatamente", "A cada 5 minutos", "A cada 15 minutos", "A cada hora"],
                    index=1
                )
                
                st.markdown("#### Som")
                som_notif = st.checkbox("Tocar som nas notificações", value=False)
                
                if som_notif:
                    volume = st.slider("Volume", 0, 100, 50)
        
        # Resumo de notificações
        st.markdown("### 📊 Resumo de Notificações")
        
        notif_data = pd.DataFrame({
            'Tipo': ['Anomalias', 'Alertas', 'Relatórios', 'Sistema'],
            'Últimas 24h': [12, 3, 1, 2],
            'Última Semana': [67, 15, 7, 5],
            'Último Mês': [234, 48, 30, 12]
        })
        
        st.dataframe(notif_data, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Configurações de Dados e API")
        
        # Configurações de cache
        st.markdown("### 💾 Cache e Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cache_ativo = st.checkbox("Ativar cache de dados", value=True)
            
            if cache_ativo:
                cache_tempo = st.select_slider(
                    "Tempo de vida do cache",
                    options=["5 min", "15 min", "30 min", "1 hora", "6 horas", "24 horas"],
                    value="30 min"
                )
                
                cache_size = st.number_input(
                    "Tamanho máximo do cache (MB)",
                    min_value=100,
                    max_value=5000,
                    value=500,
                    step=100
                )
        
        with col2:
            st.markdown("#### Status do Cache")
            st.markdown("""
            <div style="background: #F3F4F6; padding: 15px; border-radius: 8px;">
                <div style="margin-bottom: 10px;">
                    <span style="color: #6B7280;">Uso atual:</span>
                    <strong style="color: #047857; float: right;">234 MB / 500 MB</strong>
                </div>
                <div style="background: #E5E7EB; height: 8px; border-radius: 4px;">
                    <div style="background: #10B981; height: 8px; width: 47%; border-radius: 4px;"></div>
                </div>
                <button style="margin-top: 10px; padding: 5px 15px; background: #EF4444; 
                              color: white; border: none; border-radius: 6px; cursor: pointer;">
                    🗑️ Limpar Cache
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        # API Settings
        st.markdown("### 🔌 Configurações da API")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Limites de Requisição")
            
            rate_limit = st.number_input(
                "Requisições por minuto",
                min_value=10,
                max_value=1000,
                value=100,
                step=10
            )
            
            timeout = st.number_input(
                "Timeout (segundos)",
                min_value=5,
                max_value=120,
                value=30,
                step=5
            )
        
        with col2:
            st.markdown("#### Autenticação")
            
            api_key = st.text_input("Chave da API", value="****-****-****-****", type="password")
            
            if st.button("🔄 Gerar Nova Chave"):
                st.success("Nova chave gerada com sucesso!")
        
        # Data sources
        st.markdown("### 📊 Fontes de Dados")
        
        sources_data = pd.DataFrame({
            'Fonte': ['Portal da Transparência', 'SIAFI', 'ComprasNet', 'SICONV'],
            'Status': ['✅ Ativo', '✅ Ativo', '⚠️ Limitado', '❌ Inativo'],
            'Última Sync': ['Há 2 horas', 'Há 4 horas', 'Há 1 dia', 'Há 7 dias'],
            'Registros': ['1.2M', '890K', '456K', '0']
        })
        
        st.dataframe(sources_data, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("Informações do Perfil")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Avatar placeholder
            st.markdown("""
            <div style="background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); 
                        width: 150px; height: 150px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center;
                        margin: 20px auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <span style="color: white; font-size: 48px; font-weight: bold;">AH</span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📷 Alterar Foto", use_container_width=True):
                st.info("Funcionalidade em desenvolvimento")
        
        with col2:
            st.markdown("### 👤 Dados Pessoais")
            
            nome = st.text_input("Nome completo", value="Anderson Henrique Silva")
            email_perfil = st.text_input("Email", value="anderson.h.silva95@gmail.com")
            cargo = st.text_input("Cargo", value="Analista de Dados")
            organizacao = st.text_input("Organização", value="TransparenciaBR")
            
            st.markdown("### 🌐 Redes Sociais")
            
            linkedin = st.text_input("LinkedIn", value="https://www.linkedin.com/in/anderson-h-silva95/")
            github = st.text_input("GitHub", value="https://github.com/andersonhsilva")
        
        # Estatísticas do usuário
        st.markdown("### 📊 Suas Estatísticas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;
                        border: 1px solid #E5E7EB;">
                <h3 style="color: #3B82F6; margin: 0;">156</h3>
                <p style="color: #6B7280; margin: 5px 0 0 0; font-size: 12px;">Análises realizadas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;
                        border: 1px solid #E5E7EB;">
                <h3 style="color: #10B981; margin: 0;">89</h3>
                <p style="color: #6B7280; margin: 5px 0 0 0; font-size: 12px;">Anomalias detectadas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;
                        border: 1px solid #E5E7EB;">
                <h3 style="color: #F59E0B; margin: 0;">34</h3>
                <p style="color: #6B7280; margin: 5px 0 0 0; font-size: 12px;">Relatórios gerados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;
                        border: 1px solid #E5E7EB;">
                <h3 style="color: #8B5CF6; margin: 0;">412h</h3>
                <p style="color: #6B7280; margin: 5px 0 0 0; font-size: 12px;">Tempo de uso</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.subheader("Segurança e Privacidade")
        
        # Alteração de senha
        st.markdown("### 🔐 Alterar Senha")
        
        col1, col2 = st.columns(2)
        
        with col1:
            senha_atual = st.text_input("Senha atual", type="password")
            nova_senha = st.text_input("Nova senha", type="password")
            confirmar_senha = st.text_input("Confirmar nova senha", type="password")
            
            if st.button("🔄 Alterar Senha"):
                if nova_senha == confirmar_senha:
                    st.success("Senha alterada com sucesso!")
                else:
                    st.error("As senhas não coincidem!")
        
        with col2:
            st.markdown("#### Requisitos de Senha")
            st.markdown("""
            <div style="background: #F3F4F6; padding: 15px; border-radius: 8px;">
                <ul style="color: #6B7280; margin: 0; padding-left: 20px;">
                    <li>Mínimo 8 caracteres</li>
                    <li>Pelo menos uma letra maiúscula</li>
                    <li>Pelo menos uma letra minúscula</li>
                    <li>Pelo menos um número</li>
                    <li>Pelo menos um caractere especial</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Autenticação de dois fatores
        st.markdown("### 🛡️ Autenticação de Dois Fatores")
        
        two_factor = st.checkbox("Ativar autenticação de dois fatores", value=False)
        
        if two_factor:
            metodo_2fa = st.radio(
                "Método de autenticação",
                ["📱 SMS", "📧 Email", "🔐 App Autenticador"],
                index=2
            )
            
            if metodo_2fa == "📱 SMS":
                telefone = st.text_input("Número de telefone", value="+55 11 98765-4321")
            elif metodo_2fa == "🔐 App Autenticador":
                st.info("Escaneie o QR Code com seu app autenticador")
                # QR Code placeholder
                st.markdown("""
                <div style="background: white; padding: 20px; border-radius: 8px; 
                            border: 1px solid #E5E7EB; text-align: center;">
                    <div style="width: 150px; height: 150px; background: #F3F4F6; 
                                margin: 0 auto; display: flex; align-items: center; 
                                justify-content: center; border-radius: 8px;">
                        <span style="color: #6B7280;">QR Code</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Log de atividades
        st.markdown("### 📋 Log de Atividades Recentes")
        
        atividades_data = pd.DataFrame({
            'Data/Hora': ['27/05/2025 14:32', '27/05/2025 10:15', '26/05/2025 16:45', 
                         '26/05/2025 09:30', '25/05/2025 18:20'],
            'Atividade': ['Login realizado', 'Relatório exportado', 'Senha alterada', 
                         'Configurações atualizadas', 'Análise executada'],
            'IP': ['192.168.1.100', '192.168.1.100', '192.168.1.100', 
                   '192.168.1.100', '192.168.1.100'],
            'Status': ['✅ Sucesso', '✅ Sucesso', '✅ Sucesso', '✅ Sucesso', '✅ Sucesso']
        })
        
        st.dataframe(atividades_data, use_container_width=True, hide_index=True)
        
        # Sessões ativas
        st.markdown("### 💻 Sessões Ativas")
        
        sessoes_data = pd.DataFrame({
            'Dispositivo': ['Chrome - Windows', 'Safari - MacOS', 'App Mobile - Android'],
            'Localização': ['São Paulo, BR', 'São Paulo, BR', 'São Paulo, BR'],
            'Última Atividade': ['Agora', 'Há 15 minutos', 'Há 2 horas'],
            'Ação': ['Sessão Atual', 'Encerrar', 'Encerrar']
        })
        
        st.dataframe(sessoes_data, use_container_width=True, hide_index=True)
    
    # Botões de ação no final
    st.markdown("<hr style='margin: 30px 0; border: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💾 Salvar Configurações", type="primary", use_container_width=True):
            st.success("Configurações salvas com sucesso!")
    
    with col2:
        if st.button("↩️ Restaurar Padrões", use_container_width=True):
            st.info("Configurações restauradas aos valores padrão")
    
    with col3:
        st.markdown("""
        <div style="text-align: right; color: #6B7280; padding-top: 8px;">
            Última atualização: 27/05/2025 às 14:32
        </div>
        """, unsafe_allow_html=True)