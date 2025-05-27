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
    
    # Header
    st.markdown("## 🏠 Visão Geral")
    st.markdown("Bem-vindo ao TransparenciaBR Analytics! Este dashboard fornece insights sobre os gastos públicos do Governo Federal.")
    
    # Métricas principais
    st.markdown("### 📊 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Métricas mockadas (substituir por dados reais quando disponível)
    with col1:
        st.metric(
            label="Total de Contratos",
            value="12.456",
            delta="↑ 234 este mês",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Valor Total (2024)",
            value="R$ 45,8 Bi",
            delta="↑ 12% vs 2023",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Fornecedores Ativos",
            value="8.923",
            delta="↑ 156 novos",
            delta_color="normal"
        )
    
    with col4:
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
        
        fig.update_layout(
            showlegend=False,
            height=300,
            xaxis_title="",
            yaxis_title="Bilhões (R$)",
            hovermode='x unified'
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
            title="",
            color='Valor',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            showlegend=False,
            height=300,
            xaxis_title="Bilhões (R$)",
            yaxis_title="",
            coloraxis_showscale=False
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
    st.markdown("### 🔔 Alertas Recentes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("💡 **Novo padrão detectado**: Aumento de 15% nos contratos de TI no último mês")
        st.warning("⚠️ **Atenção**: 3 fornecedores com contratos vencendo esta semana")
    
    with col2:
        st.success("✅ **Coleta concluída**: 45.678 novos registros de pagamentos processados")
        st.error("❌ **Erro na coleta**: Endpoint de servidores indisponível há 2 dias")
    
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