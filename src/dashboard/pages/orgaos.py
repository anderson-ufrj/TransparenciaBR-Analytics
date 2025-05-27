"""Página de órgãos públicos."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_orgaos_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 30px;
                border: 1px solid #E0F2FE;">
        <h2 style="color: #047857; margin-top: 0;">🏢 Análise de Órgãos Públicos</h2>
        <p style="color: #666; font-size: 1.1em; margin-bottom: 0;">Compare e analise o desempenho dos órgãos federais</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo_orgao = st.selectbox(
            "Tipo de Órgão",
            ["Todos", "Ministérios", "Autarquias", "Fundações", "Empresas Públicas"]
        )
    with col2:
        periodo = st.selectbox(
            "Período",
            ["2024", "2023", "2022", "2021", "2020"]
        )
    with col3:
        metrica = st.selectbox(
            "Métrica Principal",
            ["Orçamento Total", "Execução Orçamentária", "Nº de Contratos", "Nº de Servidores"]
        )
    
    # Dados simulados dos principais órgãos
    orgaos_data = {
        'Órgão': [
            'Ministério da Saúde', 'Ministério da Educação', 'Ministério da Defesa',
            'Ministério da Fazenda', 'Ministério da Infraestrutura', 'Ministério da Justiça',
            'Ministério da Cidadania', 'Ministério da Agricultura', 'Ministério do Meio Ambiente',
            'Ministério da Ciência e Tecnologia'
        ],
        'Orçamento (Bilhões)': [195.4, 156.8, 112.3, 98.7, 87.5, 65.4, 124.3, 45.6, 12.8, 8.9],
        'Executado (%)': [92, 88, 95, 91, 78, 89, 94, 85, 72, 68],
        'Contratos': [15234, 12456, 8976, 6543, 9876, 4567, 11234, 3456, 1234, 987],
        'Servidores': [45678, 38456, 285432, 12345, 8765, 15678, 9876, 5432, 2345, 1876],
        'Eficiência': [4.3, 4.1, 4.2, 4.5, 3.8, 4.0, 4.4, 3.9, 3.5, 3.3]
    }
    
    df_orgaos = pd.DataFrame(orgaos_data)
    
    # KPIs em cards
    st.markdown("### 📊 Visão Geral")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #A7F3D0;
                    text-align: center;">
            <h3 style="color: #047857; margin: 0; font-size: 2em;">10</h3>
            <p style="color: #065F46; margin: 5px 0;">Órgãos Principais</p>
            <p style="color: #10B981; font-size: 0.9em; margin: 0;">Ministérios e Autarquias</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_orcamento = df_orgaos['Orçamento (Bilhões)'].sum()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #FCD34D;
                    text-align: center;">
            <h3 style="color: #B45309; margin: 0; font-size: 2em;">R$ {total_orcamento:.1f}B</h3>
            <p style="color: #92400E; margin: 5px 0;">Orçamento Total</p>
            <p style="color: #F59E0B; font-size: 0.9em; margin: 0;">↑ 15% vs ano anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        media_execucao = df_orgaos['Executado (%)'].mean()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #93C5FD;
                    text-align: center;">
            <h3 style="color: #1E40AF; margin: 0; font-size: 2em;">{media_execucao:.0f}%</h3>
            <p style="color: #1E3A8A; margin: 5px 0;">Execução Média</p>
            <p style="color: #3B82F6; font-size: 0.9em; margin: 0;">Orçamento executado</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_servidores = df_orgaos['Servidores'].sum()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #D8B4FE;
                    text-align: center;">
            <h3 style="color: #7C3AED; margin: 0; font-size: 2em;">{total_servidores:,}</h3>
            <p style="color: #6B21A8; margin: 5px 0;">Servidores Ativos</p>
            <p style="color: #9333EA; font-size: 0.9em; margin: 0;">Em todos os órgãos</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs para diferentes visualizações
    st.markdown("### 📈 Análises Detalhadas")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Ranking Geral", "Orçamento", "Eficiência", "Comparação", "Mapa de Calor"])
    
    with tab1:
        # Ranking de órgãos
        st.markdown("#### 🏆 Ranking dos Órgãos por Orçamento")
        
        # Adicionar ranking
        df_orgaos['Ranking'] = range(1, len(df_orgaos) + 1)
        
        # Criar gráfico de barras horizontais
        fig_ranking = go.Figure()
        
        # Adicionar barras com cores baseadas na execução
        colors = ['#047857' if x >= 90 else '#F59E0B' if x >= 80 else '#EF4444' 
                 for x in df_orgaos['Executado (%)']]
        
        fig_ranking.add_trace(go.Bar(
            y=df_orgaos['Órgão'][::-1],
            x=df_orgaos['Orçamento (Bilhões)'][::-1],
            orientation='h',
            marker=dict(color=colors[::-1]),
            text=[f'R$ {x:.1f}B ({y}%)' for x, y in zip(
                df_orgaos['Orçamento (Bilhões)'][::-1], 
                df_orgaos['Executado (%)'][::-1]
            )],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>' +
                         'Orçamento: R$ %{x:.1f} Bilhões<br>' +
                         '<extra></extra>'
        ))
        
        fig_ranking.update_layout(
            title='Orçamento por Órgão (cor indica % de execução)',
            xaxis_title='Orçamento (R$ Bilhões)',
            yaxis_title='',
            height=600,
            margin=dict(l=250),
            font=dict(family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(0,0,0,0.1)', zeroline=False),
            yaxis=dict(showgrid=False)
        )
        
        st.plotly_chart(fig_ranking, use_container_width=True)
        
        # Legenda
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 20px; height: 20px; background: #047857; border-radius: 4px;"></div>
                <span>Execução ≥ 90%</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 20px; height: 20px; background: #F59E0B; border-radius: 4px;"></div>
                <span>Execução 80-89%</span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 20px; height: 20px; background: #EF4444; border-radius: 4px;"></div>
                <span>Execução < 80%</span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        # Análise de orçamento
        st.markdown("#### 💰 Distribuição Orçamentária")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Pie chart de distribuição
            fig_pie = px.pie(
                df_orgaos, 
                values='Orçamento (Bilhões)', 
                names='Órgão',
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                             'Orçamento: R$ %{value:.1f} Bilhões<br>' +
                             'Percentual: %{percent}<br>' +
                             '<extra></extra>'
            )
            
            fig_pie.update_layout(
                title='Distribuição do Orçamento Total',
                font=dict(family='Inter'),
                height=400
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Treemap de orçamento vs execução
            fig_treemap = px.treemap(
                df_orgaos,
                path=['Órgão'],
                values='Orçamento (Bilhões)',
                color='Executado (%)',
                color_continuous_scale='RdYlGn',
                title='Orçamento vs Execução'
            )
            
            fig_treemap.update_layout(
                font=dict(family='Inter'),
                height=400
            )
            
            st.plotly_chart(fig_treemap, use_container_width=True)
    
    with tab3:
        # Análise de eficiência
        st.markdown("#### 📊 Índice de Eficiência")
        
        # Criar scatter plot
        fig_scatter = px.scatter(
            df_orgaos,
            x='Orçamento (Bilhões)',
            y='Executado (%)',
            size='Contratos',
            color='Eficiência',
            text='Órgão',
            color_continuous_scale='Viridis',
            title='Eficiência: Orçamento vs Execução'
        )
        
        fig_scatter.update_traces(
            textposition='top center',
            textfont=dict(size=10)
        )
        
        fig_scatter.update_layout(
            xaxis_title='Orçamento (R$ Bilhões)',
            yaxis_title='Execução Orçamentária (%)',
            height=500,
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Radar chart de eficiência
        st.markdown("#### 🕸️ Perfil de Eficiência dos Top 5 Órgãos")
        
        top5_orgaos = df_orgaos.nlargest(5, 'Orçamento (Bilhões)')
        
        fig_radar = go.Figure()
        
        for _, org in top5_orgaos.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    org['Executado (%)'],
                    (org['Contratos'] / df_orgaos['Contratos'].max()) * 100,
                    (org['Servidores'] / df_orgaos['Servidores'].max()) * 100,
                    org['Eficiência'] * 20,
                    (org['Orçamento (Bilhões)'] / df_orgaos['Orçamento (Bilhões)'].max()) * 100
                ],
                theta=['Execução', 'Contratos', 'Servidores', 'Eficiência', 'Orçamento'],
                fill='toself',
                name=org['Órgão'].split()[-1]  # Pegar última palavra do nome
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            font=dict(family='Inter'),
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab4:
        # Comparação entre órgãos
        st.markdown("#### 📊 Comparação Detalhada")
        
        # Seleção de órgãos para comparar
        orgaos_selecionados = st.multiselect(
            "Selecione órgãos para comparar:",
            df_orgaos['Órgão'].tolist(),
            default=df_orgaos['Órgão'].tolist()[:3]
        )
        
        if orgaos_selecionados:
            df_comparacao = df_orgaos[df_orgaos['Órgão'].isin(orgaos_selecionados)]
            
            # Gráfico de barras agrupadas
            fig_grouped = go.Figure()
            
            metricas = {
                'Orçamento (Bilhões)': '#047857',
                'Executado (%)': '#F59E0B',
                'Eficiência': '#3B82F6'
            }
            
            for metrica, cor in metricas.items():
                if metrica == 'Eficiência':
                    valores = df_comparacao[metrica] * 20  # Escalar para visualização
                else:
                    valores = df_comparacao[metrica]
                    
                fig_grouped.add_trace(go.Bar(
                    name=metrica,
                    x=df_comparacao['Órgão'],
                    y=valores,
                    marker_color=cor
                ))
            
            fig_grouped.update_layout(
                title='Comparação entre Órgãos Selecionados',
                barmode='group',
                yaxis_title='Valores (normalizados)',
                xaxis_title='',
                font=dict(family='Inter'),
                height=400
            )
            
            st.plotly_chart(fig_grouped, use_container_width=True)
            
            # Tabela comparativa
            st.markdown("#### 📋 Tabela Comparativa")
            df_display = df_comparacao[[
                'Órgão', 'Orçamento (Bilhões)', 'Executado (%)', 
                'Contratos', 'Servidores', 'Eficiência'
            ]].copy()
            
            # Formatar valores
            df_display['Orçamento (Bilhões)'] = df_display['Orçamento (Bilhões)'].apply(lambda x: f'R$ {x:.1f}B')
            df_display['Executado (%)'] = df_display['Executado (%)'].apply(lambda x: f'{x}%')
            df_display['Contratos'] = df_display['Contratos'].apply(lambda x: f'{x:,}')
            df_display['Servidores'] = df_display['Servidores'].apply(lambda x: f'{x:,}')
            df_display['Eficiência'] = df_display['Eficiência'].apply(lambda x: f'{x:.1f}/5.0')
            
            st.dataframe(df_display, hide_index=True, use_container_width=True)
    
    with tab5:
        # Mapa de calor
        st.markdown("#### 🌡️ Mapa de Calor - Performance dos Órgãos")
        
        # Preparar dados para o heatmap
        metricas_norm = pd.DataFrame({
            'Órgão': df_orgaos['Órgão'],
            'Orçamento': (df_orgaos['Orçamento (Bilhões)'] / df_orgaos['Orçamento (Bilhões)'].max() * 100),
            'Execução': df_orgaos['Executado (%)'],
            'Contratos': (df_orgaos['Contratos'] / df_orgaos['Contratos'].max() * 100),
            'Servidores': (df_orgaos['Servidores'] / df_orgaos['Servidores'].max() * 100),
            'Eficiência': df_orgaos['Eficiência'] * 20
        })
        
        # Criar matriz para heatmap
        heatmap_data = metricas_norm.set_index('Órgão')[['Orçamento', 'Execução', 'Contratos', 'Servidores', 'Eficiência']]
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn',
            text=heatmap_data.values.round(0),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig_heatmap.update_layout(
            title='Performance Normalizada dos Órgãos (0-100)',
            xaxis_title='Métricas',
            yaxis_title='',
            height=600,
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Seção de insights
    st.markdown("### 💡 Insights e Recomendações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **🏆 Destaques Positivos:**
        - Ministério da Defesa com 95% de execução orçamentária
        - Ministério da Cidadania com melhor índice de eficiência
        - Média geral de execução acima de 85%
        """)
    
    with col2:
        st.warning("""
        **⚠️ Pontos de Atenção:**
        - Ministério do Meio Ambiente com baixa execução (72%)
        - Ministério da Infraestrutura precisa melhorar eficiência
        - Disparidade grande entre orçamentos dos órgãos
        """)