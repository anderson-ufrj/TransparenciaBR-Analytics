"""Página de fornecedores - versão corrigida."""
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
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                margin-bottom: 30px;">
        <h2 style="color: #047857; margin: 0; font-size: 32px;">
            👥 Análise de Fornecedores
        </h2>
        <p style="color: #6B7280; margin-top: 10px; margin-bottom: 0;">
            Acompanhe e avalie fornecedores do governo com dados detalhados
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #10B981; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Fornecedores Ativos</h3>
            <p style="font-size: 28px; font-weight: bold; color: #047857; margin: 5px 0;">2.347</p>
            <p style="color: #10B981; font-size: 12px; margin: 0;">↑ 5% vs ano anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #F59E0B; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Volume Contratado</h3>
            <p style="font-size: 28px; font-weight: bold; color: #D97706; margin: 5px 0;">R$ 1.2B</p>
            <p style="color: #F59E0B; font-size: 12px; margin: 0;">↑ 15% vs ano anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #3B82F6; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Taxa de Conformidade</h3>
            <p style="font-size: 28px; font-weight: bold; color: #1E40AF; margin: 5px 0;">89%</p>
            <p style="color: #3B82F6; font-size: 12px; margin: 0;">Média geral</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #EF4444; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Pendências</h3>
            <p style="font-size: 28px; font-weight: bold; color: #DC2626; margin: 5px 0;">156</p>
            <p style="color: #EF4444; font-size: 12px; margin: 0;">Documentação irregular</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Separador
    st.markdown("<hr style='margin: 30px 0; border: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Tabs de análise
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 Ranking", 
        "📊 Distribuição",
        "📈 Evolução",
        "🗺️ Mapa",
        "✅ Compliance"
    ])
    
    with tab1:
        st.subheader("Top 15 Fornecedores por Volume Contratado")
        
        # Dados simulados - corrigidos
        fornecedores_data = pd.DataFrame({
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
            'Contratos': [45, 38, 52, 31, 28, 24, 35, 19, 22, 18, 27, 15, 20, 12, 16],
            'Score': [95, 92, 88, 85, 91, 87, 83, 90, 86, 89, 82, 84, 81, 79, 77]
        })
        
        # Gráfico de barras horizontais
        fig_ranking = px.bar(fornecedores_data.head(10), 
                           x='Valor Total (R$ Mi)', 
                           y='Fornecedor',
                           orientation='h',
                           color='Valor Total (R$ Mi)',
                           color_continuous_scale='Greens',
                           title='Top 10 Fornecedores por Valor Contratado',
                           text='Valor Total (R$ Mi)')
        
        fig_ranking.update_traces(texttemplate='R$ %{text:.1f}M', textposition='outside')
        fig_ranking.update_layout(
            xaxis_title='Valor Total (R$ Milhões)',
            yaxis_title='',
            height=500,
            showlegend=False,
            yaxis={'categoryorder':'total ascending'}
        )
        
        st.plotly_chart(fig_ranking, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("### 📋 Detalhamento dos Top 15 Fornecedores")
        
        # Adicionar colunas de status
        fornecedores_data['Status'] = ['🟢 Regular' if score >= 85 else '🟡 Atenção' if score >= 75 else '🔴 Irregular' 
                                      for score in fornecedores_data['Score']]
        fornecedores_data['Ranking'] = range(1, len(fornecedores_data) + 1)
        
        # Reorganizar colunas
        cols_order = ['Ranking', 'Fornecedor', 'CNPJ', 'Valor Total (R$ Mi)', 'Contratos', 'Score', 'Status']
        st.dataframe(fornecedores_data[cols_order], use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Distribuição de Fornecedores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza - Por porte
            porte_data = pd.DataFrame({
                'Porte': ['MEI', 'ME', 'EPP', 'Demais'],
                'Quantidade': [15, 35, 30, 20]
            })
            
            fig_porte = px.pie(porte_data, values='Quantidade', names='Porte',
                             title='Distribuição por Porte',
                             color_discrete_sequence=['#10B981', '#34D399', '#6EE7B7', '#A7F3D0'])
            st.plotly_chart(fig_porte, use_container_width=True)
        
        with col2:
            # Gráfico de barras - Por setor
            setor_data = pd.DataFrame({
                'Setor': ['Tecnologia', 'Saúde', 'Construção', 'Serviços', 'Outros'],
                'Percentual': [28, 22, 20, 18, 12]
            })
            
            fig_setor = px.bar(setor_data, x='Setor', y='Percentual',
                             title='Distribuição por Setor (%)',
                             color='Percentual',
                             color_continuous_scale='Greens',
                             text='Percentual')
            fig_setor.update_traces(texttemplate='%{text}%', textposition='outside')
            fig_setor.update_layout(showlegend=False)
            st.plotly_chart(fig_setor, use_container_width=True)
    
    with tab3:
        st.subheader("Evolução Temporal")
        
        # Dados de evolução
        meses = pd.date_range('2024-01', '2024-12', freq='M')
        evolucao_data = pd.DataFrame({
            'Mês': meses,
            'Fornecedores Ativos': [2100, 2152, 2200, 2238, 2280, 2335, 2396, 2454, 2517, 2584, 2656, 2734],
            'Novos Cadastros': [45, 52, 48, 38, 42, 55, 61, 58, 63, 67, 72, 78]
        })
        
        # Gráfico de linha e barras combinado
        fig_evolucao = go.Figure()
        
        fig_evolucao.add_trace(go.Scatter(
            x=evolucao_data['Mês'],
            y=evolucao_data['Fornecedores Ativos'],
            mode='lines+markers',
            name='Total Ativos',
            line=dict(color='#047857', width=3),
            yaxis='y'
        ))
        
        fig_evolucao.add_trace(go.Bar(
            x=evolucao_data['Mês'],
            y=evolucao_data['Novos Cadastros'],
            name='Novos Cadastros',
            marker_color='#A7F3D0',
            yaxis='y2',
            opacity=0.6
        ))
        
        fig_evolucao.update_layout(
            title='Evolução do Cadastro de Fornecedores em 2024',
            xaxis_title='Mês',
            yaxis=dict(
                title='Total de Fornecedores Ativos',
                titlefont=dict(color='#047857'),
                tickfont=dict(color='#047857')
            ),
            yaxis2=dict(
                title='Novos Cadastros no Mês',
                titlefont=dict(color='#059669'),
                tickfont=dict(color='#059669'),
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with tab4:
        st.subheader("Distribuição Geográfica")
        
        # Dados por estado
        estados_data = pd.DataFrame({
            'Estado': ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'SC', 'PE', 'CE', 'GO'],
            'Fornecedores': [567, 423, 345, 289, 267, 234, 198, 176, 165, 154],
            'Valor (R$ Mi)': [234.5, 187.3, 156.2, 134.8, 123.4, 98.7, 87.6, 76.5, 65.4, 54.3]
        })
        
        # Gráfico de bolhas
        fig_mapa = px.scatter(estados_data, 
                            x='Fornecedores', 
                            y='Valor (R$ Mi)',
                            size='Fornecedores',
                            color='Valor (R$ Mi)',
                            hover_data=['Estado'],
                            title='Fornecedores por Estado',
                            color_continuous_scale='Greens',
                            labels={'Fornecedores': 'Número de Fornecedores'},
                            text='Estado')
        
        fig_mapa.update_traces(textposition='top center')
        st.plotly_chart(fig_mapa, use_container_width=True)
        
        # Tabela
        st.markdown("### 📊 Detalhamento por Estado")
        estados_data['Valor Médio (R$ Mi)'] = (estados_data['Valor (R$ Mi)'] / estados_data['Fornecedores']).round(2)
        st.dataframe(estados_data, use_container_width=True, hide_index=True)
    
    with tab5:
        st.subheader("Análise de Compliance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Gauge de compliance
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 89,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Compliance Geral (%)"},
                delta = {'reference': 85},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#047857"},
                    'steps': [
                        {'range': [0, 50], 'color': "#FEE2E2"},
                        {'range': [50, 80], 'color': "#FEF3C7"},
                        {'range': [80, 100], 'color': "#D1FAE5"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Critérios de avaliação
            criterios_data = pd.DataFrame({
                'Critério': ['Documentação', 'Fiscal', 'Qualidade', 'Prazo', 'Preço'],
                'Score': [92, 88, 85, 90, 87]
            })
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=criterios_data['Score'],
                theta=criterios_data['Critério'],
                fill='toself',
                fillcolor='rgba(4, 120, 87, 0.2)',
                line=dict(color='#047857', width=2),
                name='Score Médio'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=False,
                title='Avaliação por Critério',
                height=300
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col3:
            # Métricas de compliance
            st.markdown("""
            <div style="background: #F3F4F6; padding: 20px; border-radius: 12px;">
                <h4 style="color: #374151; margin-bottom: 15px;">📊 Métricas</h4>
                <div style="margin-bottom: 12px;">
                    <span style="color: #6B7280;">Regularizados:</span>
                    <strong style="color: #10B981; float: right;">234</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color: #6B7280;">Pendentes:</span>
                    <strong style="color: #F59E0B; float: right;">156</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color: #6B7280;">Irregulares:</span>
                    <strong style="color: #EF4444; float: right;">23</strong>
                </div>
                <div>
                    <span style="color: #6B7280;">Tempo médio:</span>
                    <strong style="color: #3B82F6; float: right;">12 dias</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Lista de pendências
        st.markdown("### ⚠️ Fornecedores com Pendências")
        
        pendencias_data = pd.DataFrame({
            'Fornecedor': ['Delta Services', 'Omega Tech', 'Sigma Logística', 'Beta Solutions', 'Alpha Corp'],
            'CNPJ': ['12.345.678/0001-00', '23.456.789/0001-00', '34.567.890/0001-00', 
                    '45.678.901/0001-00', '56.789.012/0001-00'],
            'Pendência': ['Certidão vencida', 'Doc. incompleta', 'CNDT irregular', 
                         'Balanço pendente', 'Certidão federal'],
            'Prazo': ['Vencido há 15 dias', '30 dias', 'Vencido há 7 dias', '45 dias', 'Vencido há 3 dias'],
            'Risco': ['🔴 Alto', '🟡 Médio', '🔴 Alto', '🟡 Médio', '🔴 Alto']
        })
        
        st.dataframe(pendencias_data, use_container_width=True, hide_index=True)