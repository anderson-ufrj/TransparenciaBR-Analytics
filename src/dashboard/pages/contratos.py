"""Página de contratos - versão corrigida."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_contratos_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                margin-bottom: 30px;">
        <h2 style="color: #047857; margin: 0; font-size: 32px;">
            📑 Análise de Contratos
        </h2>
        <p style="color: #6B7280; margin-top: 10px; margin-bottom: 0;">
            Acompanhe e analise contratos públicos com transparência total
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #10B981; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Contratos Ativos</h3>
            <p style="font-size: 28px; font-weight: bold; color: #047857; margin: 5px 0;">782</p>
            <p style="color: #10B981; font-size: 12px; margin: 0;">↑ 12% vs mês anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #F59E0B; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Valor Total</h3>
            <p style="font-size: 28px; font-weight: bold; color: #D97706; margin: 5px 0;">R$ 245M</p>
            <p style="color: #F59E0B; font-size: 12px; margin: 0;">↑ 8% vs mês anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #3B82F6; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Dias Médios</h3>
            <p style="font-size: 28px; font-weight: bold; color: #1E40AF; margin: 5px 0;">45</p>
            <p style="color: #3B82F6; font-size: 12px; margin: 0;">Tempo de tramitação</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #EF4444; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Alertas</h3>
            <p style="font-size: 28px; font-weight: bold; color: #DC2626; margin: 5px 0;">23</p>
            <p style="color: #EF4444; font-size: 12px; margin: 0;">Contratos vencendo</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Separador
    st.markdown("<hr style='margin: 30px 0; border: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Tabs de análise
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Evolução Temporal", 
        "📊 Por Modalidade",
        "🏢 Por Fornecedor",
        "🔥 Mapa de Calor"
    ])
    
    with tab1:
        st.subheader("Evolução de Contratos")
        
        # Dados de evolução
        meses = pd.date_range('2024-01', '2024-12', freq='M')
        evolucao_data = pd.DataFrame({
            'Mês': meses,
            'Número de Contratos': [45, 52, 48, 55, 61, 58, 63, 67, 72, 70, 75, 78],
            'Valor Total (R$ Mi)': [15.2, 18.5, 16.8, 19.2, 21.5, 20.1, 22.8, 24.3, 25.9, 25.2, 27.1, 28.5]
        })
        
        # Gráfico combinado
        fig_evolucao = go.Figure()
        
        fig_evolucao.add_trace(go.Scatter(
            x=evolucao_data['Mês'],
            y=evolucao_data['Número de Contratos'],
            mode='lines+markers',
            name='Número de Contratos',
            line=dict(color='#047857', width=3),
            yaxis='y'
        ))
        
        fig_evolucao.add_trace(go.Bar(
            x=evolucao_data['Mês'],
            y=evolucao_data['Valor Total (R$ Mi)'],
            name='Valor Total (R$ Mi)',
            marker_color='#A7F3D0',
            yaxis='y2',
            opacity=0.6
        ))
        
        fig_evolucao.update_layout(
            title='Evolução de Contratos em 2024',
            xaxis_title='Mês',
            yaxis=dict(
                title='Número de Contratos',
                titlefont=dict(color='#047857'),
                tickfont=dict(color='#047857')
            ),
            yaxis2=dict(
                title='Valor Total (R$ Mi)',
                titlefont=dict(color='#059669'),
                tickfont=dict(color='#059669'),
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with tab2:
        st.subheader("Distribuição por Modalidade")
        
        # Dados por modalidade
        modalidade_data = pd.DataFrame({
            'Modalidade': ['Pregão', 'Concorrência', 'Tomada de Preços', 'Convite', 'Dispensa'],
            'Valor (R$ Mi)': [120.5, 85.3, 45.2, 15.8, 28.7],
            'Quantidade': [234, 156, 89, 45, 123]
        })
        
        # Gráfico de pizza
        fig_modalidade = px.pie(modalidade_data, 
                              values='Valor (R$ Mi)', 
                              names='Modalidade',
                              title='Distribuição de Valor por Modalidade',
                              color_discrete_sequence=['#047857', '#059669', '#10B981', '#34D399', '#6EE7B7'])
        
        st.plotly_chart(fig_modalidade, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("### 📋 Detalhamento por Modalidade")
        st.dataframe(modalidade_data, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Top 10 Fornecedores")
        
        # Dados de fornecedores
        fornecedores_data = pd.DataFrame({
            'Fornecedor': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E', 
                          'Empresa F', 'Empresa G', 'Empresa H', 'Empresa I', 'Empresa J'],
            'Valor (R$ Mi)': [45.2, 38.7, 32.1, 28.5, 24.3, 21.8, 19.2, 16.5, 14.3, 12.1],
            'Contratos': [12, 15, 8, 10, 7, 9, 6, 5, 4, 3]
        })
        
        # Gráfico de barras horizontais
        fig_fornecedores = px.bar(fornecedores_data, 
                                 x='Valor (R$ Mi)', 
                                 y='Fornecedor',
                                 orientation='h',
                                 color='Valor (R$ Mi)',
                                 color_continuous_scale='Greens',
                                 title='Top 10 Fornecedores por Valor Contratado')
        
        fig_fornecedores.update_layout(
            xaxis_title='Valor Total (R$ Milhões)',
            yaxis_title='',
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig_fornecedores, use_container_width=True)
    
    with tab4:
        st.subheader("Mapa de Calor - Contratos por Órgão e Mês")
        
        # Dados para heatmap
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        orgaos = ['Min. Saúde', 'Min. Educação', 'Min. Fazenda', 'Min. Defesa', 'Min. Justiça']
        
        # Valores simulados
        valores = np.random.randint(5, 50, size=(len(orgaos), len(meses)))
        
        # Criar heatmap
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=valores,
            x=meses,
            y=orgaos,
            colorscale='Greens',
            text=valores,
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig_heatmap.update_layout(
            title='Distribuição de Contratos por Órgão e Mês',
            xaxis_title='Mês',
            yaxis_title='Órgão',
            height=400
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Tabela de contratos recentes
    st.markdown("### 📋 Contratos Recentes")
    
    contratos_recentes = pd.DataFrame({
        'Número': ['CT-2024-001', 'CT-2024-002', 'CT-2024-003', 'CT-2024-004', 'CT-2024-005'],
        'Fornecedor': ['Empresa Alpha', 'Beta Solutions', 'Gamma Tech', 'Delta Services', 'Epsilon Corp'],
        'Objeto': ['Serviços de TI', 'Manutenção', 'Material', 'Consultoria', 'Software'],
        'Valor': ['R$ 1.250.000', 'R$ 850.000', 'R$ 2.100.000', 'R$ 500.000', 'R$ 3.200.000'],
        'Status': ['🟢 Ativo', '🟢 Ativo', '🟡 Análise', '🟢 Ativo', '🔴 Suspenso'],
        'Vigência': ['31/12/2024', '30/06/2025', '31/03/2025', '31/12/2024', '30/09/2025']
    })
    
    st.dataframe(contratos_recentes, use_container_width=True, hide_index=True)
    
    # Alertas
    st.markdown("### ⚠️ Alertas e Notificações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("""
        **Contratos Próximos ao Vencimento**
        - CT-2024-001: Vence em 30 dias
        - CT-2024-004: Vence em 45 dias
        - CT-2024-007: Vence em 60 dias
        """)
    
    with col2:
        st.error("""
        **Contratos com Pendências**
        - CT-2024-005: Documentação incompleta
        - CT-2024-008: Aguardando aprovação
        - CT-2024-011: Valor acima do limite
        """)