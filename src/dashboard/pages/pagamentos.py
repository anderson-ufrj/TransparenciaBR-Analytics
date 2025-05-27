"""Página de pagamentos."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_pagamentos_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 30px;
                border: 1px solid #E0F2FE;">
        <h2 style="color: #047857; margin-top: 0;">💰 Análise de Pagamentos Públicos</h2>
        <p style="color: #666; font-size: 1.1em; margin-bottom: 0;">Monitore e analise o fluxo de pagamentos do governo federal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tipo_pagamento = st.selectbox(
            "Tipo de Pagamento",
            ["Todos", "Pessoal", "Fornecedores", "Benefícios", "Transferências", "Outros"]
        )
    with col2:
        orgao = st.selectbox(
            "Órgão",
            ["Todos", "Min. Saúde", "Min. Educação", "Min. Defesa", "Min. Cidadania"]
        )
    with col3:
        periodo = st.selectbox(
            "Período",
            ["Janeiro 2024", "Dezembro 2023", "Novembro 2023", "Outubro 2023"]
        )
    with col4:
        status = st.selectbox(
            "Status",
            ["Todos", "Processado", "Pendente", "Cancelado", "Em Análise"]
        )
    
    # KPIs em cards
    st.markdown("### 📊 Resumo de Pagamentos")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #A7F3D0;
                    text-align: center;">
            <h3 style="color: #047857; margin: 0; font-size: 2em;">R$ 45,8B</h3>
            <p style="color: #065F46; margin: 5px 0;">Total Pago no Mês</p>
            <p style="color: #10B981; font-size: 0.9em; margin: 0;">↑ 8% vs mês anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #93C5FD;
                    text-align: center;">
            <h3 style="color: #1E40AF; margin: 0; font-size: 2em;">124.567</h3>
            <p style="color: #1E3A8A; margin: 5px 0;">Transações</p>
            <p style="color: #3B82F6; font-size: 0.9em; margin: 0;">Processadas no período</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #FCD34D;
                    text-align: center;">
            <h3 style="color: #B45309; margin: 0; font-size: 2em;">R$ 368K</h3>
            <p style="color: #92400E; margin: 5px 0;">Valor Médio</p>
            <p style="color: #F59E0B; font-size: 0.9em; margin: 0;">Por transação</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #FCA5A5;
                    text-align: center;">
            <h3 style="color: #B91C1C; margin: 0; font-size: 2em;">287</h3>
            <p style="color: #991B1B; margin: 5px 0;">Pendentes</p>
            <p style="color: #EF4444; font-size: 0.9em; margin: 0;">Aguardando aprovação</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs para diferentes visualizações
    st.markdown("### 📈 Análises Detalhadas")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Fluxo Temporal", "Por Categoria", "Beneficiários", "Status", "Auditoria"])
    
    with tab1:
        # Fluxo de pagamentos ao longo do tempo
        st.markdown("#### 📅 Evolução Temporal dos Pagamentos")
        
        # Dados simulados
        dates = pd.date_range(start='2023-01-01', end='2024-01-31', freq='D')
        valores_diarios = np.random.normal(1500, 300, len(dates)) * 1000000  # Em milhões
        valores_diarios = np.abs(valores_diarios)  # Garantir valores positivos
        
        df_temporal = pd.DataFrame({
            'Data': dates,
            'Valor': valores_diarios,
            'Mês': dates.strftime('%Y-%m')
        })
        
        # Agregar por mês
        df_mensal = df_temporal.groupby('Mês')['Valor'].sum().reset_index()
        df_mensal['Valor_Bilhoes'] = df_mensal['Valor'] / 1e9
        
        # Gráfico de linha com área
        fig_temporal = go.Figure()
        
        fig_temporal.add_trace(go.Scatter(
            x=df_mensal['Mês'],
            y=df_mensal['Valor_Bilhoes'],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#047857', width=3),
            marker=dict(size=8, color='#047857'),
            fillcolor='rgba(4, 120, 87, 0.2)',
            name='Valor Pago'
        ))
        
        # Adicionar linha de média móvel
        df_mensal['Media_Movel'] = df_mensal['Valor_Bilhoes'].rolling(window=3, center=True).mean()
        
        fig_temporal.add_trace(go.Scatter(
            x=df_mensal['Mês'],
            y=df_mensal['Media_Movel'],
            mode='lines',
            line=dict(color='#F59E0B', width=2, dash='dash'),
            name='Média Móvel (3 meses)'
        ))
        
        fig_temporal.update_layout(
            title='Evolução Mensal dos Pagamentos',
            xaxis_title='Mês',
            yaxis_title='Valor (R$ Bilhões)',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter'),
            height=500
        )
        
        st.plotly_chart(fig_temporal, use_container_width=True)
        
        # Mini cards com estatísticas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Média Mensal", f"R$ {df_mensal['Valor_Bilhoes'].mean():.1f}B")
        with col2:
            st.metric("Maior Mês", f"R$ {df_mensal['Valor_Bilhoes'].max():.1f}B")
        with col3:
            st.metric("Menor Mês", f"R$ {df_mensal['Valor_Bilhoes'].min():.1f}B")
        with col4:
            st.metric("Variação", f"{((df_mensal['Valor_Bilhoes'].iloc[-1] / df_mensal['Valor_Bilhoes'].iloc[-2] - 1) * 100):.1f}%")
    
    with tab2:
        # Análise por categoria
        st.markdown("#### 📂 Distribuição por Categoria")
        
        categorias_data = {
            'Categoria': ['Pessoal e Encargos', 'Benefícios Previdenciários', 'Transferências', 
                         'Custeio', 'Investimentos', 'Fornecedores', 'Outros'],
            'Valor': [125.4, 98.7, 67.3, 45.2, 23.8, 34.5, 15.9],
            'Quantidade': [45678, 234567, 12345, 8976, 3456, 6789, 4567],
            'Crescimento': [5.2, 8.1, -2.3, 12.5, -15.6, 7.8, 3.2]
        }
        
        df_categorias = pd.DataFrame(categorias_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de barras horizontais
            fig_barras = go.Figure()
            
            # Cores baseadas no crescimento
            colors = ['#047857' if x >= 0 else '#EF4444' for x in df_categorias['Crescimento']]
            
            fig_barras.add_trace(go.Bar(
                y=df_categorias['Categoria'],
                x=df_categorias['Valor'],
                orientation='h',
                marker=dict(color=colors),
                text=[f'R$ {v:.1f}B ({c:+.1f}%)' for v, c in zip(df_categorias['Valor'], df_categorias['Crescimento'])],
                textposition='outside'
            ))
            
            fig_barras.update_layout(
                title='Pagamentos por Categoria (variação % vs mês anterior)',
                xaxis_title='Valor (R$ Bilhões)',
                yaxis_title='',
                height=400,
                margin=dict(l=200),
                font=dict(family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_barras, use_container_width=True)
        
        with col2:
            # Donut chart
            fig_donut = go.Figure(data=[go.Pie(
                labels=df_categorias['Categoria'],
                values=df_categorias['Valor'],
                hole=0.4,
                marker_colors=px.colors.sequential.Greens_r
            )])
            
            fig_donut.update_layout(
                title='Proporção por Categoria',
                annotations=[dict(
                    text='R$ 410.8B',
                    x=0.5, y=0.5,
                    font_size=20,
                    showarrow=False
                )],
                showlegend=False,
                font=dict(family='Inter'),
                height=400
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
    
    with tab3:
        # Top beneficiários
        st.markdown("#### 🏆 Maiores Beneficiários")
        
        # Dados simulados de beneficiários
        beneficiarios_data = {
            'Beneficiário': [
                'Prefeitura Municipal de São Paulo',
                'Estado do Rio de Janeiro',
                'Prefeitura Municipal do Rio de Janeiro',
                'Estado de Minas Gerais',
                'Prefeitura Municipal de Brasília',
                'Hospital Federal XYZ',
                'Universidade Federal ABC',
                'Instituto Nacional DEF',
                'Fundação GHI',
                'Empresa Pública JKL'
            ],
            'CNPJ': [
                '46.395.000/0001-39',
                '42.498.650/0001-48',
                '42.498.733/0001-48',
                '18.715.615/0001-60',
                '00.394.601/0001-26',
                '12.345.678/0001-90',
                '23.456.789/0001-01',
                '34.567.890/0001-12',
                '45.678.901/0001-23',
                '56.789.012/0001-34'
            ],
            'Valor_Recebido': [2345.6, 1987.3, 1456.8, 1234.5, 987.6, 765.4, 543.2, 432.1, 321.0, 234.5],
            'Num_Pagamentos': [1234, 987, 765, 654, 543, 432, 321, 234, 187, 156],
            'Tipo': ['Municipal', 'Estadual', 'Municipal', 'Estadual', 'Municipal', 
                    'Federal', 'Federal', 'Federal', 'Federal', 'Federal']
        }
        
        df_beneficiarios = pd.DataFrame(beneficiarios_data)
        
        # Gráfico de barras dos top 10
        fig_top = go.Figure()
        
        # Cores por tipo
        color_map = {'Municipal': '#047857', 'Estadual': '#F59E0B', 'Federal': '#3B82F6'}
        colors = [color_map[tipo] for tipo in df_beneficiarios['Tipo']]
        
        fig_top.add_trace(go.Bar(
            x=df_beneficiarios['Beneficiário'],
            y=df_beneficiarios['Valor_Recebido'],
            marker=dict(color=colors),
            text=[f'R$ {v:.1f}M' for v in df_beneficiarios['Valor_Recebido']],
            textposition='outside'
        ))
        
        fig_top.update_layout(
            title='Top 10 Beneficiários por Valor Recebido',
            xaxis_title='',
            yaxis_title='Valor Recebido (R$ Milhões)',
            xaxis_tickangle=-45,
            height=500,
            font=dict(family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Legenda dos tipos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 20px; height: 20px; background: #047857; border-radius: 4px;"></div>
                <span>Municipal</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 20px; height: 20px; background: #F59E0B; border-radius: 4px;"></div>
                <span>Estadual</span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 20px; height: 20px; background: #3B82F6; border-radius: 4px;"></div>
                <span>Federal</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabela detalhada
        st.markdown("#### 📋 Detalhamento dos Beneficiários")
        df_display = df_beneficiarios.copy()
        df_display['Valor_Recebido'] = df_display['Valor_Recebido'].apply(lambda x: f'R$ {x:,.1f} M')
        df_display['Num_Pagamentos'] = df_display['Num_Pagamentos'].apply(lambda x: f'{x:,}')
        
        st.dataframe(df_display, hide_index=True, use_container_width=True)
    
    with tab4:
        # Status dos pagamentos
        st.markdown("#### 📦 Status dos Pagamentos")
        
        # Dados de status
        status_data = {
            'Status': ['Processado', 'Pendente', 'Em Análise', 'Cancelado', 'Devolvido'],
            'Quantidade': [112345, 287, 1543, 234, 98],
            'Valor': [42.5, 2.3, 0.8, 0.15, 0.05],
            'Percentual': [92.1, 2.3, 1.3, 0.2, 0.1]
        }
        
        df_status = pd.DataFrame(status_data)
        
        # Gauge charts para cada status
        fig_gauges = go.Figure()
        
        # Criar subplots para gauges
        from plotly.subplots import make_subplots
        
        fig_gauges = make_subplots(
            rows=1, cols=5,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}, 
                   {'type': 'indicator'}, {'type': 'indicator'}]],
            column_titles=['Processado', 'Pendente', 'Em Análise', 'Cancelado', 'Devolvido']
        )
        
        colors = ['#047857', '#F59E0B', '#3B82F6', '#EF4444', '#6B7280']
        
        for i, (status, perc, cor) in enumerate(zip(df_status['Status'], df_status['Percentual'], colors)):
            fig_gauges.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=perc,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    number={'suffix': "%"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': cor},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 100], 'color': 'lightgray'}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90}}
                ),
                row=1, col=i+1
            )
        
        fig_gauges.update_layout(
            height=300,
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_gauges, use_container_width=True)
        
        # Timeline de processamento
        st.markdown("#### ⏱️ Tempo Médio de Processamento")
        
        processos = ['Aprovação', 'Verificação', 'Autorização', 'Liquidação', 'Pagamento']
        tempos = [2.5, 1.2, 3.8, 0.5, 1.0]
        
        fig_timeline = go.Figure(go.Bar(
            x=tempos,
            y=processos,
            orientation='h',
            marker=dict(
                color=tempos,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Dias")
            ),
            text=[f'{t:.1f} dias' for t in tempos],
            textposition='outside'
        ))
        
        fig_timeline.update_layout(
            title='Tempo Médio por Etapa do Processo',
            xaxis_title='Tempo (dias)',
            yaxis_title='',
            height=400,
            font=dict(family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab5:
        # Auditoria e compliance
        st.markdown("#### 🔍 Auditoria e Compliance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Indicadores de auditoria
            st.markdown("""
            <div style="background: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #374151; margin: 0 0 15px 0;">Indicadores de Conformidade</h4>
                <div style="display: grid; gap: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #6B7280;">Documentação Completa</span>
                        <span style="color: #047857; font-weight: 700;">98.5%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #6B7280;">Aprovações em Dia</span>
                        <span style="color: #047857; font-weight: 700;">95.2%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #6B7280;">Sem Irregularidades</span>
                        <span style="color: #F59E0B; font-weight: 700;">89.7%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #6B7280;">Auditados</span>
                        <span style="color: #3B82F6; font-weight: 700;">76.3%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Alertas de auditoria
            st.markdown("""
            <div style="background: #FEF2F2; padding: 20px; border-radius: 12px; border: 1px solid #FECACA;">
                <h4 style="color: #991B1B; margin: 0 0 15px 0;">⚠️ Alertas de Auditoria</h4>
                <ul style="margin: 0; padding-left: 20px; color: #7F1D1D;">
                    <li style="margin-bottom: 8px;">15 pagamentos acima de R$ 10M sem aprovação adicional</li>
                    <li style="margin-bottom: 8px;">8 beneficiários com documentação vencida</li>
                    <li style="margin-bottom: 8px;">23 transações com valores duplicados</li>
                    <li>5 pagamentos para contas não verificadas</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Histórico de auditoria
        st.markdown("#### 📅 Histórico de Auditorias")
        
        auditorias_data = {
            'Data': ['2024-01-15', '2023-12-20', '2023-11-18', '2023-10-22', '2023-09-15'],
            'Tipo': ['Completa', 'Parcial', 'Completa', 'Emergencial', 'Parcial'],
            'Pagamentos Analisados': [15678, 8934, 14567, 2345, 7890],
            'Irregularidades': [23, 5, 18, 45, 12],
            'Status': ['Concluída', 'Concluída', 'Concluída', 'Concluída', 'Em Andamento']
        }
        
        df_auditorias = pd.DataFrame(auditorias_data)
        
        # Adicionar ícones de status
        df_auditorias['Status Visual'] = df_auditorias['Status'].map({
            'Concluída': '🟢',
            'Em Andamento': '🟡',
            'Pendente': '🔴'
        })
        
        # Formatar números
        df_display = df_auditorias.copy()
        df_display['Pagamentos Analisados'] = df_display['Pagamentos Analisados'].apply(lambda x: f'{x:,}')
        df_display = df_display[['Status Visual', 'Data', 'Tipo', 'Pagamentos Analisados', 'Irregularidades', 'Status']]
        df_display.columns = ['', 'Data', 'Tipo', 'Pagamentos', 'Irregularidades', 'Status']
        
        st.dataframe(df_display, hide_index=True, use_container_width=True)
    
    # Seção de insights
    st.markdown("### 💡 Insights e Recomendações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **🏆 Pontos Positivos:**
        - Taxa de processamento acima de 92%
        - Tempo médio de pagamento reduzido em 15%
        - 98.5% dos pagamentos com documentação completa
        - Redução de 30% em pagamentos cancelados
        """)
    
    with col2:
        st.warning("""
        **🔍 Áreas de Melhoria:**
        - 287 pagamentos pendentes há mais de 30 dias
        - Aumentar taxa de auditoria para 90%
        - Reduzir tempo de aprovação em 20%
        - Implementar validação automática de duplicatas
        """)