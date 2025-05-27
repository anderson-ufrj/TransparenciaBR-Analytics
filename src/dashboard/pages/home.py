"""
Página inicial do dashboard com métricas gerais e visão geral do sistema.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import json

def render_home_page():
    """Renderiza a página inicial do dashboard."""
    
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 30px;
                border: 1px solid #E0F2FE;">
        <h2 style="color: #047857; margin-top: 0;">🏠 Visão Geral</h2>
        <p style="color: #374151; font-size: 1.1rem; margin-bottom: 0;">
            Bem-vindo ao <strong style="color: #059669;">TransparenciaBR Analytics</strong>! 
            Este dashboard fornece insights detalhados sobre os gastos públicos do Governo Federal Brasileiro,
            promovendo transparência e facilitando o controle social.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principais com ícones
    st.markdown("""
    <h3 style="color: #047857; margin-bottom: 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Bandeira_do_Brasil.png/30px-Bandeira_do_Brasil.png" 
             style="vertical-align: middle; margin-right: 10px;">
        Métricas Principais
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Métricas mockadas com estilo brasileiro
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; color: #059669;">📑</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Total de Contratos",
            value="12.456",
            delta="↑ 234 este mês",
            delta_color="normal"
        )
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; color: #EAB308;">💰</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Valor Total (2024)",
            value="R$ 45,8 Bi",
            delta="↑ 12% vs 2023",
            delta_color="normal"
        )
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; color: #3B82F6;">🏢</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Fornecedores Ativos",
            value="8.923",
            delta="↑ 156 novos",
            delta_color="normal"
        )
    
    with col4:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; color: #059669;">🏛️</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Órgãos Monitorados",
            value="387",
            delta="100% cobertura",
            delta_color="off"
        )
    
    st.markdown("---")
    
    # Gráficos de visão geral
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Evolução de Gastos (Últimos 12 meses)")
        
        # Dados mockados para demonstração
        months = pd.date_range(end=datetime.now(), periods=12, freq='M')
        values = [45.2, 48.3, 46.7, 51.2, 49.8, 52.3, 50.1, 53.4, 51.9, 54.2, 52.8, 55.6]
        
        df_gastos = pd.DataFrame({
            'Mês': months,
            'Valor (Bilhões)': values
        })
        
        fig = px.line(
            df_gastos, 
            x='Mês', 
            y='Valor (Bilhões)',
            title="",
            line_shape='spline',
            markers=True
        )
        
        fig.update_traces(
            line_color='#059669',
            line_width=3,
            marker_size=8,
            marker_color='#047857'
        )
        
        fig.update_layout(
            showlegend=False,
            height=300,
            xaxis_title="",
            yaxis_title="Bilhões (R$)",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(229, 231, 235, 0.5)'),
            yaxis=dict(gridcolor='rgba(229, 231, 235, 0.5)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏢 Top 5 Órgãos por Gastos")
        
        # Dados mockados
        orgaos_data = {
            'Órgão': ['Min. Saúde', 'Min. Educação', 'Min. Defesa', 'Min. Infraestrutura', 'Min. Desenvolvimento'],
            'Valor': [125.4, 98.7, 76.3, 54.2, 43.1]
        }
        
        df_orgaos = pd.DataFrame(orgaos_data)
        
        fig = px.bar(
            df_orgaos,
            x='Valor',
            y='Órgão',
            orientation='h',
            title=""
        )
        
        # Cores gradientes verde e amarelo (cores do Brasil)
        colors = ['#059669', '#10B981', '#34D399', '#6EE7B7', '#A7F3D0']
        
        fig.update_traces(
            marker_color=colors,
            marker_line_color='#047857',
            marker_line_width=1
        )
        
        fig.update_layout(
            showlegend=False,
            height=300,
            xaxis_title="Bilhões (R$)",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(229, 231, 235, 0.5)'),
            yaxis=dict(gridcolor='rgba(229, 231, 235, 0.5)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Status da coleta de dados
    st.markdown("### 🔄 Status da Coleta de Dados")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tabela de status
        status_data = {
            'Endpoint': ['Contratos', 'Pagamentos', 'Licitações', 'Fornecedores', 'Servidores'],
            'Última Coleta': [
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                (datetime.now() - timedelta(hours=2)).strftime("%d/%m/%Y %H:%M"),
                (datetime.now() - timedelta(hours=5)).strftime("%d/%m/%Y %H:%M"),
                (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y %H:%M"),
                (datetime.now() - timedelta(days=2)).strftime("%d/%m/%Y %H:%M")
            ],
            'Status': ['✅ Atualizado', '✅ Atualizado', '⚠️ Atualizando', '✅ Atualizado', '❌ Desatualizado'],
            'Registros': ['12.456', '234.567', '45.678', '8.923', '567.890']
        }
        
        df_status = pd.DataFrame(status_data)
        
        # Estilizar tabela
        st.dataframe(
            df_status,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Status da última coleta",
                    width="medium",
                ),
                "Registros": st.column_config.NumberColumn(
                    "Registros",
                    help="Total de registros coletados",
                    format="%s",
                ),
            }
        )
    
    with col2:
        # Gráfico de pizza do status
        status_counts = df_status['Status'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=['Atualizado', 'Atualizando', 'Desatualizado'],
            values=[3, 1, 1],
            hole=.3,
            marker_colors=['#28a745', '#ffc107', '#dc3545']
        )])
        
        fig.update_layout(
            showlegend=True,
            height=250,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Alertas e notificações
    st.markdown("---")
    st.markdown("""
    <h3 style="color: #047857; margin-bottom: 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/30px-Flag_of_Brazil.svg.png" 
             style="vertical-align: middle; margin-right: 10px;">
        Alertas e Notificações
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #EFF6FF; border-left: 4px solid #3B82F6; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
            <strong style="color: #1E40AF;">💡 Novo padrão detectado</strong><br>
            <span style="color: #3730A3;">Aumento de 15% nos contratos de TI no último mês</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; border-radius: 8px;">
            <strong style="color: #D97706;">⚠️ Atenção</strong><br>
            <span style="color: #92400E;">3 fornecedores com contratos vencendo esta semana</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #D1FAE5; border-left: 4px solid #10B981; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
            <strong style="color: #047857;">✅ Coleta concluída</strong><br>
            <span style="color: #065F46;">45.678 novos registros de pagamentos processados</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #FEE2E2; border-left: 4px solid #EF4444; padding: 15px; border-radius: 8px;">
            <strong style="color: #DC2626;">❌ Erro na coleta</strong><br>
            <span style="color: #991B1B;">Endpoint de servidores indisponível há 2 dias</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("---")
    st.markdown("### ⚡ Ações Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            st.info("Iniciando coleta de dados...")
    
    with col2:
        if st.button("📊 Gerar Relatório", use_container_width=True):
            st.info("Gerando relatório...")
    
    with col3:
        if st.button("🔍 Detectar Anomalias", use_container_width=True):
            st.info("Analisando anomalias...")
    
    with col4:
        if st.button("📧 Enviar Alertas", use_container_width=True):
            st.info("Enviando alertas...")