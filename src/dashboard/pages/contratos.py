"""Página de contratos."""
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
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 30px;
                border: 1px solid #E0F2FE;">
        <h2 style="color: #047857; margin-top: 0;">📑 Análise de Contratos Governamentais</h2>
        <p style="color: #666; font-size: 1.1em; margin-bottom: 0;">Acompanhe e analise contratos públicos com transparência total</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        orgao = st.selectbox(
            "Órgão",
            ["Todos", "Ministério da Saúde", "Ministério da Educação", "Ministério da Fazenda"]
        )
    with col2:
        status = st.selectbox(
            "Status",
            ["Todos", "Ativo", "Encerrado", "Suspenso"]
        )
    with col3:
        modalidade = st.selectbox(
            "Modalidade",
            ["Todas", "Pregão", "Concorrência", "Dispensa"]
        )
    with col4:
        ano = st.selectbox(
            "Ano",
            ["2024", "2023", "2022", "2021"]
        )
    
    # Dados simulados
    np.random.seed(42)
    contratos_data = {
        'mes': pd.date_range('2024-01', '2024-12', freq='M'),
        'numero_contratos': [45, 52, 48, 55, 61, 58, 63, 67, 72, 70, 75, 78],
        'valor_total': [15.2, 18.5, 16.8, 19.2, 21.5, 20.1, 22.8, 24.3, 25.9, 25.2, 27.1, 28.5]
    }
    df_contratos = pd.DataFrame(contratos_data)
    
    # KPIs em cards
    st.markdown("### 📊 Indicadores Principais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #A7F3D0;
                    text-align: center;">
            <h3 style="color: #047857; margin: 0; font-size: 2em;">782</h3>
            <p style="color: #065F46; margin: 5px 0;">Contratos Ativos</p>
            <p style="color: #10B981; font-size: 0.9em; margin: 0;">↑ 12% vs mês anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #FCD34D;
                    text-align: center;">
            <h3 style="color: #B45309; margin: 0; font-size: 2em;">R$ 245M</h3>
            <p style="color: #92400E; margin: 5px 0;">Valor Total</p>
            <p style="color: #F59E0B; font-size: 0.9em; margin: 0;">↑ 8% vs mês anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #93C5FD;
                    text-align: center;">
            <h3 style="color: #1E40AF; margin: 0; font-size: 2em;">45</h3>
            <p style="color: #1E3A8A; margin: 5px 0;">Dias Médios</p>
            <p style="color: #3B82F6; font-size: 0.9em; margin: 0;">Tempo de tramitação</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #FCA5A5;
                    text-align: center;">
            <h3 style="color: #B91C1C; margin: 0; font-size: 2em;">23</h3>
            <p style="color: #991B1B; margin: 5px 0;">Alertas</p>
            <p style="color: #EF4444; font-size: 0.9em; margin: 0;">Contratos vencendo</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos
    st.markdown("### 📈 Análises Detalhadas")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Evolução Temporal", "Por Modalidade", "Por Fornecedor", "Mapa de Calor"])
    
    with tab1:
        # Gráfico de evolução temporal
        fig_evolucao = go.Figure()
        
        # Número de contratos
        fig_evolucao.add_trace(go.Scatter(
            x=df_contratos['mes'],
            y=df_contratos['numero_contratos'],
            name='Número de Contratos',
            mode='lines+markers',
            line=dict(color='#047857', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))
        
        # Valor total
        fig_evolucao.add_trace(go.Bar(
            x=df_contratos['mes'],
            y=df_contratos['valor_total'],
            name='Valor Total (R$ Mi)',
            marker_color='#A7F3D0',
            yaxis='y2',
            opacity=0.7
        ))
        
        fig_evolucao.update_layout(
            title='Evolução de Contratos ao Longo do Ano',
            xaxis_title='Mês',
            yaxis=dict(
                title='Número de Contratos',
                titlefont=dict(color='#047857'),
                tickfont=dict(color='#047857')
            ),
            yaxis2=dict(
                title='Valor Total (R$ Milhões)',
                titlefont=dict(color='#059669'),
                tickfont=dict(color='#059669'),
                anchor='free',
                overlaying='y',
                side='right',
                position=0.95
            ),
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with tab2:
        # Gráfico por modalidade
        modalidades = ['Pregão', 'Concorrência', 'Tomada de Preços', 'Convite', 'Dispensa']
        valores = [120.5, 85.3, 45.2, 15.8, 28.7]
        cores = ['#047857', '#059669', '#10B981', '#34D399', '#6EE7B7']
        
        fig_modalidade = go.Figure(data=[go.Pie(
            labels=modalidades,
            values=valores,
            hole=0.3,
            marker_colors=cores
        )])
        
        fig_modalidade.update_layout(
            title='Distribuição de Contratos por Modalidade',
            annotations=[dict(text='R$ 295.5M', x=0.5, y=0.5, font_size=20, showarrow=False)],
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_modalidade, use_container_width=True)
    
    with tab3:
        # Top fornecedores
        fornecedores_data = {
            'fornecedor': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E', 
                          'Empresa F', 'Empresa G', 'Empresa H', 'Empresa I', 'Empresa J'],
            'valor': [45.2, 38.7, 32.1, 28.5, 24.3, 21.8, 19.2, 16.5, 14.3, 12.1],
            'contratos': [12, 15, 8, 10, 7, 9, 6, 5, 4, 3]
        }
        df_fornecedores = pd.DataFrame(fornecedores_data)
        
        fig_fornecedores = go.Figure()
        
        fig_fornecedores.add_trace(go.Bar(
            x=df_fornecedores['valor'],
            y=df_fornecedores['fornecedor'],
            orientation='h',
            marker=dict(
                color=df_fornecedores['valor'],
                colorscale=[[0, '#D1FAE5'], [1, '#047857']],
                showscale=True,
                colorbar=dict(title="Valor (R$ Mi)")
            ),
            text=df_fornecedores['valor'].apply(lambda x: f'R$ {x:.1f}M'),
            textposition='outside'
        ))
        
        fig_fornecedores.update_layout(
            title='Top 10 Fornecedores por Valor Contratado',
            xaxis_title='Valor Total (R$ Milhões)',
            yaxis_title='',
            height=500,
            margin=dict(l=150),
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_fornecedores, use_container_width=True)
    
    with tab4:
        # Mapa de calor
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        orgaos = ['Min. Saúde', 'Min. Educação', 'Min. Fazenda', 'Min. Defesa', 'Min. Justiça']
        
        # Dados simulados para o mapa de calor
        valores_heatmap = np.random.randint(5, 50, size=(len(orgaos), len(meses)))
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=valores_heatmap,
            x=meses,
            y=orgaos,
            colorscale=[[0, '#ECFDF5'], [0.5, '#6EE7B7'], [1, '#047857']],
            text=valores_heatmap,
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig_heatmap.update_layout(
            title='Distribuição de Contratos por Órgão e Mês',
            xaxis_title='Mês',
            yaxis_title='Órgão',
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Tabela de contratos recentes
    st.markdown("### 📋 Contratos Recentes")
    
    contratos_recentes = {
        'Número': ['CT-2024-001', 'CT-2024-002', 'CT-2024-003', 'CT-2024-004', 'CT-2024-005'],
        'Fornecedor': ['Empresa Alpha', 'Beta Solutions', 'Gamma Tech', 'Delta Services', 'Epsilon Corp'],
        'Objeto': ['Serviços de TI', 'Manutenção predial', 'Fornecimento de material', 'Consultoria', 'Desenvolvimento de software'],
        'Valor': ['R$ 1.250.000,00', 'R$ 850.000,00', 'R$ 2.100.000,00', 'R$ 500.000,00', 'R$ 3.200.000,00'],
        'Status': ['🟢 Ativo', '🟢 Ativo', '🟡 Em análise', '🟢 Ativo', '🔴 Suspenso'],
        'Vigência': ['31/12/2024', '30/06/2025', '31/03/2025', '31/12/2024', '30/09/2025']
    }
    
    df_recentes = pd.DataFrame(contratos_recentes)
    
    # Estilizar tabela
    st.markdown("""
    <style>
        .dataframe {
            border: none !important;
        }
        .dataframe td, .dataframe th {
            border: none !important;
            padding: 12px !important;
        }
        .dataframe tr:nth-child(even) {
            background-color: #F0F9FF;
        }
        .dataframe tr:hover {
            background-color: #E0F2FE;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(df_recentes, hide_index=True, use_container_width=True)
    
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
        - CT-2024-008: Aguardando aprovação jurídica
        - CT-2024-011: Valor acima do limite
        """)