"""Página de fornecedores."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_fornecedores_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 30px;
                border: 1px solid #E0F2FE;">
        <h2 style="color: #047857; margin-top: 0;">👥 Análise de Fornecedores</h2>
        <p style="color: #666; font-size: 1.1em; margin-bottom: 0;">Acompanhe e avalie fornecedores do governo com dados detalhados</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tipo_pessoa = st.selectbox(
            "Tipo de Pessoa",
            ["Todos", "Pessoa Jurídica", "Pessoa Física"]
        )
    with col2:
        porte = st.selectbox(
            "Porte da Empresa",
            ["Todos", "MEI", "ME", "EPP", "Demais"]
        )
    with col3:
        setor = st.selectbox(
            "Setor",
            ["Todos", "Tecnologia", "Saúde", "Construção", "Serviços"]
        )
    with col4:
        periodo = st.selectbox(
            "Período",
            ["2024", "2023", "2022", "2021"]
        )
    
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
            <h3 style="color: #047857; margin: 0; font-size: 2em;">2.347</h3>
            <p style="color: #065F46; margin: 5px 0;">Fornecedores Ativos</p>
            <p style="color: #10B981; font-size: 0.9em; margin: 0;">↑ 5% vs ano anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #FCD34D;
                    text-align: center;">
            <h3 style="color: #B45309; margin: 0; font-size: 2em;">R$ 1.2B</h3>
            <p style="color: #92400E; margin: 5px 0;">Volume Contratado</p>
            <p style="color: #F59E0B; font-size: 0.9em; margin: 0;">↑ 15% vs ano anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #93C5FD;
                    text-align: center;">
            <h3 style="color: #1E40AF; margin: 0; font-size: 2em;">89%</h3>
            <p style="color: #1E3A8A; margin: 5px 0;">Taxa de Conformidade</p>
            <p style="color: #3B82F6; font-size: 0.9em; margin: 0;">Média geral</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #FCA5A5;
                    text-align: center;">
            <h3 style="color: #B91C1C; margin: 0; font-size: 2em;">156</h3>
            <p style="color: #991B1B; margin: 5px 0;">Pendências</p>
            <p style="color: #EF4444; font-size: 0.9em; margin: 0;">Documentação irregular</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Ranking", "Distribuição", "Evolução", "Mapa", "Compliance"])
    
    with tab1:
        # Ranking de fornecedores
        st.markdown("#### 🏆 Top 15 Fornecedores por Volume Contratado")
        
        fornecedores_top = {
            'Ranking': range(1, 16),
            'Fornecedor': [
                'Tech Solutions Brasil Ltda', 'Construtora Alpha S.A.', 'MedSupply Comércio',
                'Serviços Beta EIRELI', 'Gamma Tecnologia', 'Delta Consultoria',
                'Epsilon Logística', 'Zeta Engenharia', 'Eta Manutenção',
                'Theta Sistemas', 'Iota Transportes', 'Kappa Alimentos',
                'Lambda Segurança', 'Mu Telecom', 'Nu Energia'
            ],
            'CNPJ': [
                '12.345.678/0001-00', '23.456.789/0001-00', '34.567.890/0001-00',
                '45.678.901/0001-00', '56.789.012/0001-00', '67.890.123/0001-00',
                '78.901.234/0001-00', '89.012.345/0001-00', '90.123.456/0001-00',
                '01.234.567/0001-00', '12.345.678/0001-00', '23.456.789/0001-00',
                '34.567.890/0001-00', '45.678.901/0001-00', '56.789.012/0001-00'
            ],
            'Valor Total (R$ Mi)': [125.3, 98.7, 87.5, 76.2, 65.8, 54.3, 48.9, 42.1, 38.7, 35.2, 31.8, 28.4, 25.9, 23.1, 20.5],
            'Nº Contratos': [45, 38, 52, 31, 28, 24, 35, 19, 22, 18, 27, 15, 20, 12, 16],
            'Score': [95, 92, 88, 85, 91, 87, 83, 90, 86, 89, 82, 84, 81, 79, 77]
        }
        
        df_ranking = pd.DataFrame(fornecedores_top)
        
        # Criar gráfico de barras horizontais com gradiente
        fig_ranking = go.Figure()
        
        # Adicionar barras
        fig_ranking.add_trace(go.Bar(
            y=df_ranking['Fornecedor'][::-1],  # Inverter ordem para maior no topo
            x=df_ranking['Valor Total (R$ Mi)'][::-1],
            orientation='h',
            marker=dict(
                color=df_ranking['Valor Total (R$ Mi)'][::-1],
                colorscale=[[0, '#D1FAE5'], [0.5, '#6EE7B7'], [1, '#047857']],
                showscale=True,
                colorbar=dict(
                    title="Valor<br>(R$ Mi)",
                    titleside="right",
                    tickmode="linear",
                    tick0=0,
                    dtick=25
                )
            ),
            text=[f'R$ {x:.1f}M' for x in df_ranking['Valor Total (R$ Mi)'][::-1]],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>' +
                         'Valor Total: R$ %{x:.1f} Mi<br>' +
                         '<extra></extra>'
        ))
        
        fig_ranking.update_layout(
            xaxis_title='Valor Total Contratado (R$ Milhões)',
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
        
        # Tabela detalhada
        st.markdown("#### 📊 Detalhamento dos Fornecedores")
        
        # Adicionar colunas de status
        df_ranking['Status'] = ['🟢 Regular' if score >= 85 else '🟡 Atenção' if score >= 75 else '🔴 Irregular' 
                               for score in df_ranking['Score']]
        df_ranking['Tendência'] = ['↑' if i % 3 == 0 else '→' if i % 3 == 1 else '↓' for i in range(len(df_ranking))]
        
        # Estilizar tabela
        st.dataframe(
            df_ranking[['Ranking', 'Fornecedor', 'CNPJ', 'Valor Total (R$ Mi)', 'Nº Contratos', 'Score', 'Status', 'Tendência']],
            hide_index=True,
            use_container_width=True,
            height=400
        )
    
    with tab2:
        # Distribuições
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por porte
            portes = ['MEI', 'ME', 'EPP', 'Demais']
            valores_porte = [15, 35, 30, 20]
            cores_porte = ['#6EE7B7', '#34D399', '#10B981', '#047857']
            
            fig_porte = go.Figure(data=[go.Pie(
                labels=portes,
                values=valores_porte,
                hole=0.3,
                marker_colors=cores_porte,
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig_porte.update_layout(
                title='Distribuição por Porte',
                annotations=[dict(text='Porte', x=0.5, y=0.5, font_size=16, showarrow=False)],
                font=dict(family='Inter'),
                height=400
            )
            
            st.plotly_chart(fig_porte, use_container_width=True)
        
        with col2:
            # Distribuição por setor
            setores = ['Tecnologia', 'Saúde', 'Construção', 'Serviços', 'Outros']
            valores_setor = [28, 22, 20, 18, 12]
            
            fig_setor = go.Figure(data=[go.Bar(
                x=setores,
                y=valores_setor,
                marker=dict(
                    color=valores_setor,
                    colorscale=[[0, '#D1FAE5'], [1, '#047857']],
                    showscale=False
                ),
                text=[f'{v}%' for v in valores_setor],
                textposition='outside'
            )])
            
            fig_setor.update_layout(
                title='Distribuição por Setor (%)',
                xaxis_title='',
                yaxis_title='Percentual',
                font=dict(family='Inter'),
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(gridcolor='rgba(0,0,0,0.1)', zeroline=False),
                xaxis=dict(showgrid=False)
            )
            
            st.plotly_chart(fig_setor, use_container_width=True)
    
    with tab3:
        # Evolução temporal
        meses = pd.date_range('2024-01', '2024-12', freq='M')
        novos_fornecedores = [45, 52, 48, 38, 42, 55, 61, 58, 63, 67, 72, 78]
        fornecedores_ativos = [2100, 2152, 2200, 2238, 2280, 2335, 2396, 2454, 2517, 2584, 2656, 2734]
        
        fig_evolucao = go.Figure()
        
        # Fornecedores ativos (linha)
        fig_evolucao.add_trace(go.Scatter(
            x=meses,
            y=fornecedores_ativos,
            name='Fornecedores Ativos',
            mode='lines+markers',
            line=dict(color='#047857', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))
        
        # Novos fornecedores (barras)
        fig_evolucao.add_trace(go.Bar(
            x=meses,
            y=novos_fornecedores,
            name='Novos Fornecedores',
            marker_color='#A7F3D0',
            yaxis='y2',
            opacity=0.7
        ))
        
        fig_evolucao.update_layout(
            title='Evolução do Cadastro de Fornecedores',
            xaxis_title='Mês',
            yaxis=dict(
                title='Total de Fornecedores Ativos',
                titlefont=dict(color='#047857'),
                tickfont=dict(color='#047857')
            ),
            yaxis2=dict(
                title='Novos Fornecedores no Mês',
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
            font=dict(family='Inter'),
            height=500
        )
        
        st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with tab4:
        # Mapa de distribuição por estado
        st.markdown("#### 🗺️ Distribuição Geográfica de Fornecedores")
        
        # Dados simulados por estado
        estados_data = {
            'Estado': ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'SC', 'PE', 'CE', 'GO', 'DF', 'ES', 'PA', 'MA', 'RN'],
            'Fornecedores': [567, 423, 345, 289, 267, 234, 198, 176, 165, 154, 143, 132, 121, 98, 87],
            'Valor (R$ Mi)': [234.5, 187.3, 156.2, 134.8, 123.4, 98.7, 87.6, 76.5, 65.4, 54.3, 48.9, 43.2, 37.8, 32.1, 28.7]
        }
        
        df_estados = pd.DataFrame(estados_data)
        
        # Criar mapa de bolhas
        fig_mapa = go.Figure()
        
        # Adicionar bolhas para cada estado
        fig_mapa.add_trace(go.Scatter(
            x=df_estados['Estado'],
            y=['Brasil'] * len(df_estados),
            mode='markers',
            marker=dict(
                size=df_estados['Fornecedores'] / 10,  # Escala para tamanho visual
                color=df_estados['Valor (R$ Mi)'],
                colorscale=[[0, '#D1FAE5'], [0.5, '#6EE7B7'], [1, '#047857']],
                showscale=True,
                colorbar=dict(title="Valor<br>(R$ Mi)"),
                sizemode='diameter',
                sizeref=0.5,
                line=dict(width=2, color='#047857')
            ),
            text=[f"{estado}<br>Fornecedores: {forn}<br>Valor: R$ {valor:.1f}M" 
                  for estado, forn, valor in zip(df_estados['Estado'], df_estados['Fornecedores'], df_estados['Valor (R$ Mi)'])],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        fig_mapa.update_layout(
            title='',
            xaxis_title='Estado',
            yaxis_title='',
            height=400,
            font=dict(family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        
        st.plotly_chart(fig_mapa, use_container_width=True)
        
        # Tabela com detalhes por estado
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(
                df_estados.sort_values('Fornecedores', ascending=False),
                hide_index=True,
                use_container_width=True,
                height=300
            )
        with col2:
            st.info("""
            **Legenda:**
            - Tamanho da bolha: Número de fornecedores
            - Cor da bolha: Volume contratado
            - Estados com maior concentração: SP, RJ, MG
            """)
    
    with tab5:
        # Compliance e avaliação
        st.markdown("#### 📋 Análise de Compliance e Avaliação")
        
        # Métricas de compliance
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Gauge chart para compliance geral
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=89,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Compliance Geral (%)"},
                delta={'reference': 85, 'increasing': {'color': "green"}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#047857"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': '#FEE2E2'},
                        {'range': [50, 75], 'color': '#FEF3C7'},
                        {'range': [75, 100], 'color': '#D1FAE5'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}
            ))
            
            fig_gauge.update_layout(height=300, font=dict(family='Inter'))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Distribuição de scores
            scores = np.random.normal(85, 10, 1000)
            scores = np.clip(scores, 0, 100)
            
            fig_hist = go.Figure(data=[go.Histogram(
                x=scores,
                nbinsx=20,
                marker_color='#047857',
                opacity=0.7
            )])
            
            fig_hist.update_layout(
                title='Distribuição de Scores',
                xaxis_title='Score de Compliance',
                yaxis_title='Frequência',
                height=300,
                font=dict(family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col3:
            # Critérios de avaliação
            criterios = ['Documentação', 'Regularidade Fiscal', 'Qualidade', 'Prazo', 'Preço']
            valores_criterios = [92, 88, 85, 90, 87]
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=valores_criterios,
                theta=criterios,
                fill='toself',
                fillcolor='rgba(4, 120, 87, 0.2)',
                line=dict(color='#047857', width=2)
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                title='Média por Critério',
                height=300,
                font=dict(family='Inter')
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # Lista de fornecedores com pendências
        st.markdown("#### ⚠️ Fornecedores com Pendências")
        
        pendencias_data = {
            'Fornecedor': ['Delta Services', 'Omega Tech', 'Sigma Logística', 'Beta Solutions', 'Alpha Construções'],
            'CNPJ': ['45.678.901/0001-00', '56.789.012/0001-00', '67.890.123/0001-00', '78.901.234/0001-00', '89.012.345/0001-00'],
            'Tipo de Pendência': ['Certidão vencida', 'Documentação incompleta', 'CNDT irregular', 'Balanço não apresentado', 'Certidão federal vencida'],
            'Prazo': ['Vencido há 15 dias', '30 dias para regularizar', 'Vencido há 7 dias', '45 dias para regularizar', 'Vencido há 3 dias'],
            'Risco': ['🔴 Alto', '🟡 Médio', '🔴 Alto', '🟡 Médio', '🔴 Alto']
        }
        
        df_pendencias = pd.DataFrame(pendencias_data)
        
        st.dataframe(
            df_pendencias,
            hide_index=True,
            use_container_width=True
        )
        
        # Alertas e recomendações
        col1, col2 = st.columns(2)
        
        with col1:
            st.warning("""
            **Ações Recomendadas:**
            - Notificar fornecedores com certidões vencidas
            - Bloquear novos contratos para fornecedores irregulares
            - Agendar reunião com fornecedores de alto risco
            """)
        
        with col2:
            st.success("""
            **Melhorias Recentes:**
            - 15 fornecedores regularizaram documentação
            - Score médio aumentou 3% no último mês
            - Tempo médio de regularização: 12 dias
            """)