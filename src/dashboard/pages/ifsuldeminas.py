"""Página dedicada ao IFSULDEMINAS."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_ifsuldeminas_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #DCFCE7 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                margin-bottom: 30px;">
        <h2 style="color: #14532D; margin: 0; font-size: 32px;">
            🎓 IFSULDEMINAS - Instituto Federal do Sul de Minas
        </h2>
        <p style="color: #4B5563; margin-top: 10px; margin-bottom: 0;">
            Análise detalhada de contratos, licitações e gastos por campus
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seletor de campus
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        campus_selecionado = st.selectbox(
            "Selecione o Campus",
            ["Todos os Campi", "Muzambinho", "Machado", "Inconfidentes", 
             "Poços de Caldas", "Pouso Alegre", "Passos", "Três Corações", "Carmo de Minas"]
        )
    
    with col2:
        periodo = st.selectbox(
            "Período de Análise",
            ["2024", "2023", "2022", "Últimos 3 anos"]
        )
    
    with col3:
        tipo_despesa = st.selectbox(
            "Tipo de Despesa",
            ["Todas", "Custeio", "Capital", "Pessoal"]
        )
    
    with col4:
        modalidade = st.selectbox(
            "Modalidade",
            ["Todas", "Pregão", "Dispensa", "Inexigibilidade"]
        )
    
    # KPIs principais do IFSULDEMINAS
    st.markdown("### 📊 Indicadores Gerais - IFSULDEMINAS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #10B981; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Orçamento Total</h3>
            <p style="font-size: 28px; font-weight: bold; color: #047857; margin: 5px 0;">R$ 245M</p>
            <p style="color: #10B981; font-size: 12px; margin: 0;">↑ 8% vs ano anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #3B82F6; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Alunos Atendidos</h3>
            <p style="font-size: 28px; font-weight: bold; color: #1E40AF; margin: 5px 0;">15.234</p>
            <p style="color: #3B82F6; font-size: 12px; margin: 0;">Em todos os campi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #F59E0B; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Contratos Ativos</h3>
            <p style="font-size: 28px; font-weight: bold; color: #D97706; margin: 5px 0;">234</p>
            <p style="color: #F59E0B; font-size: 12px; margin: 0;">Distribuídos em 8 campi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #8B5CF6; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Investimento/Aluno</h3>
            <p style="font-size: 28px; font-weight: bold; color: #7C3AED; margin: 5px 0;">R$ 16.087</p>
            <p style="color: #8B5CF6; font-size: 12px; margin: 0;">Média anual</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Separador
    st.markdown("<hr style='margin: 30px 0; border: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Tabs de análise
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏛️ Por Campus", 
        "💰 Orçamento",
        "📋 Licitações",
        "📑 Contratos",
        "🎯 Indicadores",
        "📊 Comparativo"
    ])
    
    with tab1:
        st.subheader("Distribuição por Campus")
        
        # Dados dos campi
        campi_data = pd.DataFrame({
            'Campus': ['Muzambinho', 'Machado', 'Inconfidentes', 'Poços de Caldas', 
                      'Pouso Alegre', 'Passos', 'Três Corações', 'Carmo de Minas'],
            'Orçamento (R$ Mi)': [45.2, 38.7, 35.4, 32.1, 28.5, 24.3, 21.8, 19.0],
            'Alunos': [2834, 2456, 2234, 1987, 1876, 1654, 1432, 761],
            'Servidores': [234, 215, 198, 187, 165, 154, 132, 87],
            'Contratos': [34, 29, 27, 25, 22, 19, 17, 11]
        })
        
        # Mapa de bolhas - Orçamento vs Alunos
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_bubble = px.scatter(campi_data, 
                                  x='Alunos', 
                                  y='Orçamento (R$ Mi)',
                                  size='Servidores',
                                  color='Campus',
                                  title='Relação Orçamento x Alunos por Campus',
                                  hover_data=['Contratos'],
                                  color_discrete_sequence=px.colors.qualitative.Set3)
            
            fig_bubble.update_layout(
                xaxis_title='Número de Alunos',
                yaxis_title='Orçamento (R$ Milhões)',
                height=500
            )
            
            st.plotly_chart(fig_bubble, use_container_width=True)
        
        with col2:
            # Card de destaque
            st.markdown("""
            <div style="background: #F0FDF4; padding: 20px; border-radius: 12px; border: 2px solid #BBF7D0;">
                <h4 style="color: #14532D; margin-bottom: 15px;">🏆 Campus Destaque</h4>
                <p style="color: #166534; font-weight: bold; font-size: 18px; margin: 5px 0;">Muzambinho</p>
                <ul style="color: #4B5563; margin: 10px 0; padding-left: 20px;">
                    <li>Maior orçamento: R$ 45.2M</li>
                    <li>2.834 alunos atendidos</li>
                    <li>234 servidores</li>
                    <li>Eficiência: 94%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabela detalhada
        st.markdown("### 📊 Dados Detalhados por Campus")
        
        # Adicionar colunas calculadas
        campi_data['Orçamento/Aluno'] = (campi_data['Orçamento (R$ Mi)'] * 1000000 / campi_data['Alunos']).round(2)
        campi_data['Alunos/Servidor'] = (campi_data['Alunos'] / campi_data['Servidores']).round(1)
        
        st.dataframe(campi_data, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Análise Orçamentária")
        
        # Evolução orçamentária
        anos = [2020, 2021, 2022, 2023, 2024]
        orcamento_total = [198.5, 205.3, 218.7, 226.4, 245.0]
        
        fig_orcamento = go.Figure()
        
        # Linha de evolução
        fig_orcamento.add_trace(go.Scatter(
            x=anos,
            y=orcamento_total,
            mode='lines+markers',
            name='Orçamento Total',
            line=dict(color='#047857', width=3),
            marker=dict(size=10)
        ))
        
        # Adicionar anotações com valores
        for i, (ano, valor) in enumerate(zip(anos, orcamento_total)):
            fig_orcamento.add_annotation(
                x=ano, y=valor,
                text=f'R$ {valor}M',
                showarrow=False,
                yshift=15,
                font=dict(size=12, color='#047857')
            )
        
        fig_orcamento.update_layout(
            title='Evolução Orçamentária do IFSULDEMINAS (2020-2024)',
            xaxis_title='Ano',
            yaxis_title='Orçamento (R$ Milhões)',
            height=400
        )
        
        st.plotly_chart(fig_orcamento, use_container_width=True)
        
        # Distribuição por tipo de despesa
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza - Tipos de despesa
            despesas_data = pd.DataFrame({
                'Tipo': ['Pessoal', 'Custeio', 'Capital', 'Assistência Estudantil', 'Outros'],
                'Valor': [145.8, 65.3, 22.1, 8.5, 3.3]
            })
            
            fig_despesas = px.pie(despesas_data, 
                                values='Valor', 
                                names='Tipo',
                                title='Distribuição por Tipo de Despesa (2024)',
                                color_discrete_sequence=['#047857', '#10B981', '#34D399', '#6EE7B7', '#A7F3D0'])
            
            st.plotly_chart(fig_despesas, use_container_width=True)
        
        with col2:
            # Execução orçamentária
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #374151; margin-bottom: 20px;">📊 Execução Orçamentária</h4>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #6B7280;">Empenhado</span>
                        <strong style="color: #047857;">89%</strong>
                    </div>
                    <div style="background: #E5E7EB; height: 8px; border-radius: 4px;">
                        <div style="background: #10B981; height: 8px; width: 89%; border-radius: 4px;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #6B7280;">Liquidado</span>
                        <strong style="color: #3B82F6;">76%</strong>
                    </div>
                    <div style="background: #E5E7EB; height: 8px; border-radius: 4px;">
                        <div style="background: #3B82F6; height: 8px; width: 76%; border-radius: 4px;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #6B7280;">Pago</span>
                        <strong style="color: #F59E0B;">68%</strong>
                    </div>
                    <div style="background: #E5E7EB; height: 8px; border-radius: 4px;">
                        <div style="background: #F59E0B; height: 8px; width: 68%; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Licitações do IFSULDEMINAS")
        
        # Estatísticas de licitações
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Licitações", "156", "↑ 12%")
        with col2:
            st.metric("Em Andamento", "23", "↓ 5%")
        with col3:
            st.metric("Valor Total", "R$ 45.6M", "↑ 18%")
        with col4:
            st.metric("Taxa de Sucesso", "92%", "↑ 3%")
        
        # Gráfico de barras - Licitações por modalidade e campus
        licitacoes_campus = pd.DataFrame({
            'Campus': ['Muzambinho', 'Machado', 'Inconfidentes', 'Poços de Caldas', 'Pouso Alegre'],
            'Pregão': [23, 19, 17, 15, 14],
            'Dispensa': [12, 10, 8, 7, 6],
            'Inexigibilidade': [4, 3, 3, 2, 2],
            'Tomada de Preços': [2, 2, 1, 1, 1]
        })
        
        fig_licitacoes = go.Figure()
        
        modalidades = ['Pregão', 'Dispensa', 'Inexigibilidade', 'Tomada de Preços']
        cores = ['#047857', '#10B981', '#34D399', '#6EE7B7']
        
        for modalidade, cor in zip(modalidades, cores):
            fig_licitacoes.add_trace(go.Bar(
                name=modalidade,
                x=licitacoes_campus['Campus'],
                y=licitacoes_campus[modalidade],
                marker_color=cor
            ))
        
        fig_licitacoes.update_layout(
            title='Licitações por Modalidade e Campus',
            barmode='stack',
            xaxis_title='Campus',
            yaxis_title='Número de Licitações',
            height=400
        )
        
        st.plotly_chart(fig_licitacoes, use_container_width=True)
        
        # Tabela de licitações recentes
        st.markdown("### 📋 Licitações Recentes")
        
        licitacoes_recentes = pd.DataFrame({
            'Processo': ['PE 23/2024', 'PE 22/2024', 'DL 45/2024', 'PE 21/2024', 'TP 03/2024'],
            'Campus': ['Muzambinho', 'Machado', 'Poços de Caldas', 'Pouso Alegre', 'Inconfidentes'],
            'Objeto': ['Material de laboratório', 'Equipamentos de TI', 'Serviços de limpeza', 
                      'Mobiliário escolar', 'Reforma de telhado'],
            'Valor Estimado': ['R$ 234.500', 'R$ 456.789', 'R$ 89.000', 'R$ 167.890', 'R$ 345.678'],
            'Status': ['🟢 Homologada', '🟡 Em análise', '🟢 Homologada', '🔵 Aberta', '🟡 Em análise']
        })
        
        st.dataframe(licitacoes_recentes, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("Contratos Ativos")
        
        # Filtros adicionais
        col1, col2 = st.columns(2)
        with col1:
            tipo_contrato = st.multiselect(
                "Tipo de Contrato",
                ["Serviços Contínuos", "Fornecimento", "Obras", "Locação"],
                default=["Serviços Contínuos", "Fornecimento"]
            )
        with col2:
            status_contrato = st.multiselect(
                "Status",
                ["Ativo", "Próximo ao vencimento", "Em renovação"],
                default=["Ativo"]
            )
        
        # Gráfico de sunburst - Hierarquia de contratos
        contratos_hierarquia = pd.DataFrame({
            'Campus': ['Muzambinho']*4 + ['Machado']*4 + ['Inconfidentes']*4,
            'Tipo': ['Serviços', 'Serviços', 'Fornecimento', 'Locação']*3,
            'Fornecedor': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D']*3,
            'Valor': [234500, 167890, 345678, 123456]*3
        })
        
        fig_sunburst = px.sunburst(
            contratos_hierarquia,
            path=['Campus', 'Tipo', 'Fornecedor'],
            values='Valor',
            title='Distribuição Hierárquica de Contratos',
            color_discrete_sequence=px.colors.sequential.Greens
        )
        
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Lista de contratos críticos
        st.markdown("### ⚠️ Contratos que Requerem Atenção")
        
        contratos_criticos = pd.DataFrame({
            'Contrato': ['CT-2024/045', 'CT-2024/032', 'CT-2024/018', 'CT-2024/056'],
            'Campus': ['Muzambinho', 'Poços de Caldas', 'Machado', 'Passos'],
            'Fornecedor': ['TechClean Ltda', 'SecPro Vigilância', 'FoodService S.A.', 'ManutencPred'],
            'Vencimento': ['15 dias', '22 dias', '30 dias', '45 dias'],
            'Valor Mensal': ['R$ 45.678', 'R$ 78.900', 'R$ 123.456', 'R$ 34.567'],
            'Ação': ['🔴 Renovar urgente', '🟡 Iniciar processo', '🟡 Preparar docs', '🔵 Monitorar']
        })
        
        st.dataframe(contratos_criticos, use_container_width=True, hide_index=True)
    
    with tab5:
        st.subheader("Indicadores de Desempenho")
        
        # Grid de indicadores
        col1, col2 = st.columns(2)
        
        with col1:
            # Indicadores acadêmicos
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #047857; margin-bottom: 20px;">📚 Indicadores Acadêmicos</h4>
                
                <div style="display: grid; gap: 15px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">Custo por aluno</span>
                        <strong style="color: #047857;">R$ 16.087/ano</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">Taxa de conclusão</span>
                        <strong style="color: #10B981;">78%</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">Alunos por professor</span>
                        <strong style="color: #3B82F6;">18.5</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">Cursos oferecidos</span>
                        <strong style="color: #8B5CF6;">87</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gráfico de radar - Desempenho por campus
            st.markdown("### 🎯 Desempenho Comparativo")
            
            categorias = ['Eficiência', 'Qualidade', 'Infraestrutura', 'Inovação', 'Sustentabilidade']
            
            fig_radar = go.Figure()
            
            # Dados para 3 campi principais
            fig_radar.add_trace(go.Scatterpolar(
                r=[85, 90, 88, 82, 79],
                theta=categorias,
                fill='toself',
                name='Muzambinho',
                line=dict(color='#047857')
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[82, 88, 85, 80, 83],
                theta=categorias,
                fill='toself',
                name='Machado',
                line=dict(color='#10B981')
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[80, 85, 82, 78, 81],
                theta=categorias,
                fill='toself',
                name='Inconfidentes',
                line=dict(color='#34D399')
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=True,
                height=400
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # Indicadores financeiros
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #1E40AF; margin-bottom: 20px;">💰 Indicadores Financeiros</h4>
                
                <div style="display: grid; gap: 15px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">Execução orçamentária</span>
                        <strong style="color: #047857;">89%</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">Economia em licitações</span>
                        <strong style="color: #10B981;">R$ 3.4M</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">ROI investimentos</span>
                        <strong style="color: #3B82F6;">156%</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #6B7280;">Redução de custos</span>
                        <strong style="color: #F59E0B;">12%</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Evolução de eficiência
            st.markdown("### 📈 Evolução da Eficiência")
            
            meses = pd.date_range('2024-01', '2024-12', freq='M')
            eficiencia_data = pd.DataFrame({
                'Mês': meses,
                'Eficiência (%)': [82, 83, 85, 84, 86, 87, 88, 89, 88, 90, 91, 92]
            })
            
            fig_eficiencia = px.area(
                eficiencia_data,
                x='Mês',
                y='Eficiência (%)',
                title='Evolução da Eficiência Operacional',
                color_discrete_sequence=['#047857']
            )
            
            fig_eficiencia.update_layout(
                yaxis_range=[80, 95],
                height=400
            )
            
            st.plotly_chart(fig_eficiencia, use_container_width=True)
    
    with tab6:
        st.subheader("Análise Comparativa entre Campi")
        
        # Matriz de comparação
        st.markdown("### 🔄 Matriz Comparativa de Desempenho")
        
        # Criar dados para heatmap comparativo
        indicadores = ['Orçamento/Aluno', 'Taxa Execução', 'Eficiência', 'Qualidade', 'Satisfação']
        campi = ['Muzambinho', 'Machado', 'Inconfidentes', 'Poços de Caldas', 'Pouso Alegre']
        
        # Valores normalizados (0-100)
        valores_comparativos = np.array([
            [92, 89, 87, 85, 88],  # Orçamento/Aluno
            [89, 91, 88, 86, 87],  # Taxa Execução
            [94, 90, 88, 87, 89],  # Eficiência
            [91, 89, 90, 88, 86],  # Qualidade
            [93, 91, 89, 90, 88]   # Satisfação
        ])
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=valores_comparativos,
            x=campi,
            y=indicadores,
            colorscale='Greens',
            text=valores_comparativos,
            texttemplate='%{text}',
            textfont={"size": 12}
        ))
        
        fig_heatmap.update_layout(
            title='Matriz de Desempenho por Campus',
            xaxis_title='Campus',
            yaxis_title='Indicador',
            height=400
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Rankings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #F0FDF4; padding: 20px; border-radius: 12px; border: 1px solid #BBF7D0;">
                <h4 style="color: #14532D; margin-bottom: 15px;">🏆 Ranking Geral dos Campi</h4>
                <ol style="color: #166534; margin: 0; padding-left: 20px;">
                    <li><strong>Muzambinho</strong> - Score: 92.4</li>
                    <li><strong>Machado</strong> - Score: 90.1</li>
                    <li><strong>Inconfidentes</strong> - Score: 88.5</li>
                    <li><strong>Poços de Caldas</strong> - Score: 87.2</li>
                    <li><strong>Pouso Alegre</strong> - Score: 87.6</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #FEF3C7; padding: 20px; border-radius: 12px; border: 1px solid #FDE68A;">
                <h4 style="color: #78350F; margin-bottom: 15px;">📊 Melhores Práticas</h4>
                <ul style="color: #92400E; margin: 0; padding-left: 20px;">
                    <li><strong>Muzambinho:</strong> Gestão eficiente</li>
                    <li><strong>Machado:</strong> Inovação pedagógica</li>
                    <li><strong>Poços de Caldas:</strong> Sustentabilidade</li>
                    <li><strong>Pouso Alegre:</strong> Parcerias</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Projeções
        st.markdown("### 🔮 Projeções para 2025")
        
        projecoes = pd.DataFrame({
            'Indicador': ['Orçamento Total', 'Número de Alunos', 'Contratos', 'Eficiência'],
            'Valor Atual': ['R$ 245M', '15.234', '234', '89%'],
            'Projeção 2025': ['R$ 268M', '16.500', '256', '92%'],
            'Crescimento': ['+9.4%', '+8.3%', '+9.4%', '+3.4%']
        })
        
        st.dataframe(projecoes, use_container_width=True, hide_index=True)