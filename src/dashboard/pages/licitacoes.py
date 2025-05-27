"""Página de licitações."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_licitacoes_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                margin-bottom: 30px;">
        <h2 style="color: #047857; margin: 0; font-size: 32px;">
            📋 Análise de Licitações
        </h2>
        <p style="color: #6B7280; margin-top: 10px; margin-bottom: 0;">
            Acompanhamento de processos licitatórios e contratos públicos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #10B981; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Licitações Ativas</h3>
            <p style="font-size: 28px; font-weight: bold; color: #047857; margin: 5px 0;">1.234</p>
            <p style="color: #10B981; font-size: 12px; margin: 0;">↑ 12% este mês</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #3B82F6; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Valor Total</h3>
            <p style="font-size: 28px; font-weight: bold; color: #1E40AF; margin: 5px 0;">R$ 2,5B</p>
            <p style="color: #3B82F6; font-size: 12px; margin: 0;">Em processos ativos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #F59E0B; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Taxa de Sucesso</h3>
            <p style="font-size: 28px; font-weight: bold; color: #D97706; margin: 5px 0;">87%</p>
            <p style="color: #F59E0B; font-size: 12px; margin: 0;">Processos concluídos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #EF4444; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Alertas</h3>
            <p style="font-size: 28px; font-weight: bold; color: #DC2626; margin: 5px 0;">23</p>
            <p style="color: #EF4444; font-size: 12px; margin: 0;">Requerem atenção</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Separador
    st.markdown("<hr style='margin: 30px 0; border: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Tabs de análise
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visão Geral", 
        "📈 Análise Temporal",
        "🏢 Por Modalidade",
        "📋 Status dos Processos",
        "🔍 Fornecedores"
    ])
    
    with tab1:
        st.subheader("Distribuição de Licitações por Status")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de pizza - Status das licitações
            status_data = pd.DataFrame({
                'Status': ['Em Andamento', 'Concluídas', 'Canceladas', 'Suspensas', 'Desertas'],
                'Quantidade': [456, 678, 45, 23, 32]
            })
            
            fig_pizza = px.pie(status_data, values='Quantidade', names='Status',
                             title="Status das Licitações",
                             color_discrete_map={
                                 'Em Andamento': '#3B82F6',
                                 'Concluídas': '#10B981',
                                 'Canceladas': '#EF4444',
                                 'Suspensas': '#F59E0B',
                                 'Desertas': '#6B7280'
                             })
            fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div style="background: #F3F4F6; padding: 20px; border-radius: 12px; margin-top: 50px;">
                <h4 style="color: #374151; margin-bottom: 15px;">Estatísticas Rápidas</h4>
                <div style="margin-bottom: 10px;">
                    <span style="color: #6B7280;">Tempo médio:</span>
                    <strong style="color: #047857;">45 dias</strong>
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="color: #6B7280;">Economia média:</span>
                    <strong style="color: #047857;">23%</strong>
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="color: #6B7280;">Participantes/licitação:</span>
                    <strong style="color: #047857;">8,5</strong>
                </div>
                <div>
                    <span style="color: #6B7280;">Impugnações:</span>
                    <strong style="color: #DC2626;">3,2%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Evolução Temporal das Licitações")
        
        # Gráfico de linha - Evolução mensal
        meses = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        temporal_data = pd.DataFrame({
            'Mês': meses,
            'Abertas': np.random.randint(80, 150, size=12),
            'Concluídas': np.random.randint(70, 140, size=12),
            'Canceladas': np.random.randint(5, 20, size=12)
        })
        
        fig_temporal = go.Figure()
        fig_temporal.add_trace(go.Scatter(x=temporal_data['Mês'], y=temporal_data['Abertas'],
                                         mode='lines+markers', name='Abertas',
                                         line=dict(color='#3B82F6', width=3)))
        fig_temporal.add_trace(go.Scatter(x=temporal_data['Mês'], y=temporal_data['Concluídas'],
                                         mode='lines+markers', name='Concluídas',
                                         line=dict(color='#10B981', width=3)))
        fig_temporal.add_trace(go.Scatter(x=temporal_data['Mês'], y=temporal_data['Canceladas'],
                                         mode='lines+markers', name='Canceladas',
                                         line=dict(color='#EF4444', width=3)))
        
        fig_temporal.update_layout(
            title="Evolução Mensal de Licitações (2024)",
            xaxis_title="Mês",
            yaxis_title="Quantidade",
            hovermode='x unified'
        )
        st.plotly_chart(fig_temporal, use_container_width=True)
        
        # Análise de sazonalidade
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #374151; margin-bottom: 15px;">📈 Tendências Identificadas</h4>
                <ul style="color: #6B7280; margin: 0;">
                    <li>Aumento de 35% nas licitações eletrônicas</li>
                    <li>Redução no tempo médio de conclusão</li>
                    <li>Maior participação de pequenas empresas</li>
                    <li>Crescimento em licitações sustentáveis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #374151; margin-bottom: 15px;">⚠️ Pontos de Atenção</h4>
                <ul style="color: #6B7280; margin: 0;">
                    <li>Pico de cancelamentos em junho</li>
                    <li>Redução de participantes em agosto</li>
                    <li>Atrasos em processos complexos</li>
                    <li>Necessidade de mais transparência</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Análise por Modalidade de Licitação")
        
        # Gráfico de barras - Modalidades
        modalidades_data = pd.DataFrame({
            'Modalidade': ['Pregão Eletrônico', 'Tomada de Preços', 'Concorrência', 
                          'Convite', 'Concurso', 'Leilão', 'Dispensa', 'Inexigibilidade'],
            'Quantidade': [567, 234, 189, 45, 23, 12, 456, 123],
            'Valor': [1200000000, 450000000, 800000000, 50000000, 
                     30000000, 150000000, 200000000, 180000000]
        })
        
        fig_modalidades = px.bar(modalidades_data, x='Modalidade', y='Quantidade',
                                title="Distribuição por Modalidade",
                                color='Valor',
                                color_continuous_scale='Blues',
                                labels={'Valor': 'Valor Total (R$)'})
        fig_modalidades.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_modalidades, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("### Detalhamento por Modalidade")
        modalidades_detail = modalidades_data.copy()
        modalidades_detail['Valor Médio'] = modalidades_detail['Valor'] / modalidades_detail['Quantidade']
        modalidades_detail['% do Total'] = (modalidades_detail['Quantidade'] / modalidades_detail['Quantidade'].sum() * 100).round(1)
        
        # Formatação dos valores
        modalidades_detail['Valor'] = modalidades_detail['Valor'].apply(lambda x: f"R$ {x:,.2f}")
        modalidades_detail['Valor Médio'] = modalidades_detail['Valor Médio'].apply(lambda x: f"R$ {x:,.2f}")
        modalidades_detail['% do Total'] = modalidades_detail['% do Total'].astype(str) + '%'
        
        st.dataframe(modalidades_detail, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("Acompanhamento de Status dos Processos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de funil - Pipeline de licitações
            funil_data = pd.DataFrame({
                'Fase': ['Publicadas', 'Com Propostas', 'Em Análise', 'Homologadas', 'Contratos Assinados'],
                'Quantidade': [1234, 987, 765, 543, 456]
            })
            
            fig_funil = px.funnel(funil_data, x='Quantidade', y='Fase',
                                title="Funil de Conversão de Licitações")
            st.plotly_chart(fig_funil, use_container_width=True)
        
        with col2:
            # Indicadores de desempenho
            st.markdown("""
            <div style="background: #F3F4F6; padding: 20px; border-radius: 12px;">
                <h4 style="color: #374151; margin-bottom: 20px;">Indicadores de Desempenho</h4>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #6B7280;">Taxa de Conversão</span>
                        <strong style="color: #047857;">37%</strong>
                    </div>
                    <div style="background: #E5E7EB; height: 8px; border-radius: 4px;">
                        <div style="background: #10B981; height: 8px; width: 37%; border-radius: 4px;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #6B7280;">Tempo de Ciclo</span>
                        <strong style="color: #F59E0B;">65%</strong>
                    </div>
                    <div style="background: #E5E7EB; height: 8px; border-radius: 4px;">
                        <div style="background: #F59E0B; height: 8px; width: 65%; border-radius: 4px;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #6B7280;">Conformidade</span>
                        <strong style="color: #3B82F6;">92%</strong>
                    </div>
                    <div style="background: #E5E7EB; height: 8px; border-radius: 4px;">
                        <div style="background: #3B82F6; height: 8px; width: 92%; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Alertas e pendências
        st.markdown("### ⚠️ Processos que Requerem Atenção")
        
        alertas_data = pd.DataFrame({
            'Processo': ['PE 2024/0234', 'TP 2024/0156', 'CC 2024/0089', 'PE 2024/0267'],
            'Órgão': ['Ministério da Saúde', 'DNIT', 'Petrobras', 'Correios'],
            'Valor': ['R$ 2.500.000,00', 'R$ 8.900.000,00', 'R$ 45.000.000,00', 'R$ 1.200.000,00'],
            'Prazo': ['5 dias', '2 dias', '1 dia', '8 dias'],
            'Status': ['Aguardando documentos', 'Recurso pendente', 'Análise técnica', 'Habilitação']
        })
        
        st.dataframe(alertas_data, use_container_width=True, hide_index=True)
    
    with tab5:
        st.subheader("Análise de Fornecedores")
        
        # Top fornecedores
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fornecedores_data = pd.DataFrame({
                'Fornecedor': ['Tech Solutions Ltda', 'Construtora ABC', 'Medical Supplies', 
                              'InfoSystems S.A.', 'Logística Express', 'Energia Solar Brasil',
                              'Alimentos Premium', 'Segurança Total'],
                'Contratos': [45, 38, 32, 28, 25, 22, 20, 18],
                'Valor Total': [125000000, 98000000, 87000000, 76000000, 
                               65000000, 54000000, 43000000, 32000000]
            })
            
            fig_fornecedores = px.scatter(fornecedores_data, x='Contratos', y='Valor Total',
                                         size='Valor Total', hover_data=['Fornecedor'],
                                         title="Fornecedores por Volume de Contratos e Valor",
                                         labels={'Valor Total': 'Valor Total (R$)'})
            st.plotly_chart(fig_fornecedores, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #374151; margin-bottom: 15px;">📊 Métricas de Fornecedores</h4>
                <div style="margin-bottom: 12px;">
                    <span style="color: #6B7280;">Total cadastrados:</span>
                    <strong style="color: #047857; float: right;">3.456</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color: #6B7280;">Ativos (último ano):</span>
                    <strong style="color: #047857; float: right;">892</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color: #6B7280;">Novos cadastros:</span>
                    <strong style="color: #3B82F6; float: right;">156</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color: #6B7280;">Taxa de retenção:</span>
                    <strong style="color: #10B981; float: right;">78%</strong>
                </div>
                <div>
                    <span style="color: #6B7280;">Penalizados:</span>
                    <strong style="color: #EF4444; float: right;">23</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Ranking de fornecedores
        st.markdown("### 🏆 Ranking de Desempenho de Fornecedores")
        
        ranking_data = pd.DataFrame({
            'Posição': ['🥇', '🥈', '🥉', '4º', '5º'],
            'Fornecedor': ['Tech Solutions Ltda', 'Medical Supplies', 'Construtora ABC', 
                          'InfoSystems S.A.', 'Energia Solar Brasil'],
            'Score': [98.5, 97.2, 96.8, 95.3, 94.7],
            'Entregas no Prazo': ['100%', '98%', '97%', '96%', '95%'],
            'Qualidade': ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐']
        })
        
        st.dataframe(ranking_data, use_container_width=True, hide_index=True)