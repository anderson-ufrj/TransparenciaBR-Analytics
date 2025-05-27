"""Página de detecção de anomalias."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_anomalias_page():
    # Header com card estilizado
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #FEF3C7 100%); 
                padding: 30px; 
                border-radius: 16px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                margin-bottom: 30px;">
        <h2 style="color: #92400E; margin: 0; font-size: 32px;">
            ⚠️ Detecção de Anomalias
        </h2>
        <p style="color: #78716C; margin-top: 10px; margin-bottom: 0;">
            Sistema inteligente de monitoramento e alertas de irregularidades
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs principais com alertas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #DC2626; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Alertas Críticos</h3>
            <p style="font-size: 28px; font-weight: bold; color: #DC2626; margin: 5px 0;">47</p>
            <p style="color: #EF4444; font-size: 12px; margin: 0;">↑ 23% esta semana</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #F59E0B; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Suspeitas</h3>
            <p style="font-size: 28px; font-weight: bold; color: #D97706; margin: 5px 0;">134</p>
            <p style="color: #F59E0B; font-size: 12px; margin: 0;">Em análise</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #3B82F6; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Taxa de Detecção</h3>
            <p style="font-size: 28px; font-weight: bold; color: #1E40AF; margin: 5px 0;">92%</p>
            <p style="color: #3B82F6; font-size: 12px; margin: 0;">Precisão do modelo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    border-left: 4px solid #10B981; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="color: #6B7280; font-size: 14px; margin: 0;">Resolvidos</h3>
            <p style="font-size: 28px; font-weight: bold; color: #047857; margin: 5px 0;">89</p>
            <p style="color: #10B981; font-size: 12px; margin: 0;">Últimos 30 dias</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Separador
    st.markdown("<hr style='margin: 30px 0; border: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Tabs de análise
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚨 Alertas Ativos", 
        "📊 Análise de Padrões",
        "🔍 Tipos de Anomalias",
        "📈 Evolução Temporal",
        "🎯 Ações Recomendadas"
    ])
    
    with tab1:
        st.subheader("Alertas em Tempo Real")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            severidade = st.selectbox("Severidade", ["Todas", "Crítica", "Alta", "Média", "Baixa"])
        with col2:
            tipo = st.selectbox("Tipo", ["Todos", "Financeiro", "Contratual", "Processual", "Documental"])
        with col3:
            periodo = st.selectbox("Período", ["Últimas 24h", "Última semana", "Último mês", "Último ano"])
        
        # Lista de alertas
        alertas_data = pd.DataFrame({
            'ID': ['#A0047', '#A0046', '#A0045', '#A0044', '#A0043'],
            'Severidade': ['🔴 Crítica', '🔴 Crítica', '🟡 Alta', '🟡 Alta', '🟠 Média'],
            'Tipo': ['Financeiro', 'Contratual', 'Processual', 'Financeiro', 'Documental'],
            'Descrição': [
                'Pagamento duplicado detectado - R$ 2.5M',
                'Contrato sem licitação válida',
                'Processo com prazo expirado há 15 dias',
                'Variação de preço acima de 300%',
                'Documentação incompleta em processo'
            ],
            'Órgão': ['Min. Saúde', 'DNIT', 'Correios', 'Petrobras', 'INSS'],
            'Data': ['Hoje 14:23', 'Hoje 11:45', 'Ontem 18:30', 'Ontem 09:15', '2 dias atrás'],
            'Status': ['🔍 Analisando', '⚡ Novo', '🔍 Analisando', '📋 Pendente', '✅ Em resolução']
        })
        
        # Estilização da tabela
        st.markdown("""
        <style>
        .dataframe {
            font-size: 14px;
        }
        .dataframe td {
            padding: 8px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(alertas_data, use_container_width=True, hide_index=True)
        
        # Detalhes do alerta selecionado
        st.markdown("### 📋 Detalhes do Alerta #A0047")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #DC2626; margin-bottom: 15px;">⚠️ Pagamento Duplicado Detectado</h4>
                <p style="color: #6B7280; margin-bottom: 10px;">
                    <strong>Descrição:</strong> Foram identificados dois pagamentos idênticos para o mesmo fornecedor 
                    no valor de R$ 2.500.000,00 com intervalo de apenas 3 horas.
                </p>
                <p style="color: #6B7280; margin-bottom: 10px;">
                    <strong>Fornecedor:</strong> Tech Solutions Ltda (CNPJ: 12.345.678/0001-90)
                </p>
                <p style="color: #6B7280; margin-bottom: 10px;">
                    <strong>Notas Fiscais:</strong> NF-2024-0234 e NF-2024-0235
                </p>
                <p style="color: #6B7280;">
                    <strong>Probabilidade de Fraude:</strong> <span style="color: #DC2626; font-weight: bold;">87%</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #FEF3C7; padding: 20px; border-radius: 12px;">
                <h4 style="color: #92400E; margin-bottom: 15px;">🎯 Ações Sugeridas</h4>
                <ol style="color: #78716C; margin: 0; padding-left: 20px;">
                    <li>Bloquear pagamento imediatamente</li>
                    <li>Contatar setor financeiro</li>
                    <li>Verificar outras transações do fornecedor</li>
                    <li>Abrir processo de investigação</li>
                    <li>Notificar controle interno</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Análise de Padrões Anômalos")
        
        # Heatmap de correlações
        st.markdown("### 🔥 Mapa de Calor - Correlação de Anomalias")
        
        # Dados para o heatmap
        orgaos = ['Min. Saúde', 'DNIT', 'Petrobras', 'Correios', 'INSS', 'Min. Educação']
        tipos = ['Pagamento Duplicado', 'Sobrepreço', 'Fracionamento', 'Direcionamento', 'Documentação']
        
        # Criar matriz de correlação
        valores = np.random.randint(0, 20, size=(len(orgaos), len(tipos)))
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=valores,
            x=tipos,
            y=orgaos,
            colorscale='Reds',
            text=valores,
            texttemplate='%{text}',
            textfont={"size": 12},
            hovertemplate='Órgão: %{y}<br>Tipo: %{x}<br>Ocorrências: %{z}<extra></extra>'
        ))
        
        fig_heatmap.update_layout(
            title="Distribuição de Anomalias por Órgão e Tipo",
            xaxis_title="Tipo de Anomalia",
            yaxis_title="Órgão",
            height=400
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Análise de redes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🕸️ Redes de Relacionamento Suspeitas")
            st.info("Foram identificadas 3 redes de empresas com padrões suspeitos de conluio em licitações.")
            
            # Métricas da rede
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB;">
                <h5 style="color: #374151; margin-bottom: 10px;">Rede Principal Detectada</h5>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #6B7280;">Empresas envolvidas:</span>
                    <strong style="color: #DC2626;">12</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #6B7280;">Contratos relacionados:</span>
                    <strong style="color: #F59E0B;">47</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #6B7280;">Valor total suspeito:</span>
                    <strong style="color: #DC2626;">R$ 145M</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 Padrões Identificados por ML")
            
            padroes_data = pd.DataFrame({
                'Padrão': ['Sazonalidade anormal', 'Concentração fornecedor', 'Valores atípicos', 'Timing suspeito'],
                'Ocorrências': [23, 18, 34, 15],
                'Confiança': [89, 92, 87, 94]
            })
            
            fig_padroes = px.bar(padroes_data, x='Padrão', y='Ocorrências',
                               color='Confiança',
                               title="Padrões Detectados por Machine Learning",
                               color_continuous_scale='RdYlBu_r',
                               labels={'Confiança': 'Confiança (%)'})
            st.plotly_chart(fig_padroes, use_container_width=True)
    
    with tab3:
        st.subheader("Categorização de Anomalias")
        
        # Gráfico de rosca - Distribuição por categoria
        col1, col2 = st.columns([3, 2])
        
        with col1:
            categorias_data = pd.DataFrame({
                'Categoria': ['Financeiras', 'Contratuais', 'Processuais', 'Documentais', 'Comportamentais'],
                'Quantidade': [145, 89, 67, 123, 45],
                'Percentual': [31, 19, 14, 26, 10]
            })
            
            fig_rosca = px.pie(categorias_data, values='Quantidade', names='Categoria',
                              title="Distribuição de Anomalias por Categoria",
                              hole=0.4,
                              color_discrete_map={
                                  'Financeiras': '#DC2626',
                                  'Contratuais': '#F59E0B',
                                  'Processuais': '#3B82F6',
                                  'Documentais': '#8B5CF6',
                                  'Comportamentais': '#10B981'
                              })
            fig_rosca.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_rosca, use_container_width=True)
        
        with col2:
            st.markdown("### 📌 Top 5 Anomalias Mais Frequentes")
            
            top_anomalias = pd.DataFrame({
                'Tipo': ['Sobrepreço', 'Pagamento duplicado', 'Fracionamento irregular', 
                        'Direcionamento', 'Documentação falsa'],
                'Freq': [234, 189, 156, 134, 98],
                'Impacto': ['R$ 45M', 'R$ 32M', 'R$ 28M', 'R$ 21M', 'R$ 15M']
            })
            
            for idx, row in top_anomalias.iterrows():
                st.markdown(f"""
                <div style="background: white; padding: 10px; margin-bottom: 10px; 
                            border-radius: 8px; border-left: 3px solid #DC2626;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="color: #374151;">{idx + 1}. {row['Tipo']}</strong>
                        <span style="color: #DC2626; font-weight: bold;">{row['Impacto']}</span>
                    </div>
                    <small style="color: #6B7280;">{row['Freq']} ocorrências</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Detalhamento por tipo
        st.markdown("### 🔍 Análise Detalhada por Tipo")
        
        tipo_selecionado = st.selectbox("Selecione o tipo de anomalia:", 
                                       ['Sobrepreço', 'Pagamento duplicado', 'Fracionamento irregular'])
        
        if tipo_selecionado == "Sobrepreço":
            st.markdown("""
            <div style="background: #FEF3C7; padding: 20px; border-radius: 12px; margin-top: 15px;">
                <h4 style="color: #92400E;">📊 Análise: Sobrepreço</h4>
                <p style="color: #78716C; margin-top: 10px;">
                    <strong>Definição:</strong> Valores contratados significativamente acima da média de mercado.
                </p>
                <p style="color: #78716C;">
                    <strong>Indicadores:</strong>
                    <ul style="margin-top: 5px;">
                        <li>Variação > 50% do preço de referência</li>
                        <li>Ausência de justificativa técnica</li>
                        <li>Fornecedor único em múltiplos contratos</li>
                    </ul>
                </p>
                <p style="color: #78716C;">
                    <strong>Impacto médio:</strong> R$ 192.000 por contrato
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Evolução Temporal de Anomalias")
        
        # Gráfico de área - Evolução mensal
        meses = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        evolucao_data = pd.DataFrame({
            'Mês': meses,
            'Críticas': np.random.randint(20, 50, size=12),
            'Altas': np.random.randint(40, 80, size=12),
            'Médias': np.random.randint(60, 100, size=12),
            'Baixas': np.random.randint(80, 120, size=12)
        })
        
        fig_area = go.Figure()
        
        cores = ['#DC2626', '#F59E0B', '#3B82F6', '#10B981']
        severidades = ['Críticas', 'Altas', 'Médias', 'Baixas']
        
        for i, (sev, cor) in enumerate(zip(severidades, cores)):
            fig_area.add_trace(go.Scatter(
                x=evolucao_data['Mês'],
                y=evolucao_data[sev],
                mode='lines',
                stackgroup='one',
                name=sev,
                line=dict(color=cor),
                fillcolor=cor
            ))
        
        fig_area.update_layout(
            title="Evolução Mensal de Anomalias por Severidade",
            xaxis_title="Mês",
            yaxis_title="Quantidade de Anomalias",
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig_area, use_container_width=True)
        
        # Análise de tendências
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Tendências e Previsões")
            
            # Gráfico de tendência
            tendencia_data = pd.DataFrame({
                'Mês': pd.date_range(start='2024-01-01', end='2025-03-31', freq='M'),
                'Real': list(np.random.randint(150, 250, size=12)) + [None]*3,
                'Previsto': [None]*12 + list(np.random.randint(200, 280, size=3))
            })
            
            fig_tendencia = go.Figure()
            fig_tendencia.add_trace(go.Scatter(
                x=tendencia_data['Mês'],
                y=tendencia_data['Real'],
                mode='lines+markers',
                name='Dados Reais',
                line=dict(color='#3B82F6', width=3)
            ))
            fig_tendencia.add_trace(go.Scatter(
                x=tendencia_data['Mês'][11:],
                y=[tendencia_data['Real'].iloc[11]] + list(tendencia_data['Previsto'][12:]),
                mode='lines+markers',
                name='Previsão',
                line=dict(color='#EF4444', width=3, dash='dash')
            ))
            
            fig_tendencia.update_layout(
                title="Previsão de Anomalias - Próximos 3 Meses",
                xaxis_title="Período",
                yaxis_title="Total de Anomalias",
                showlegend=True
            )
            
            st.plotly_chart(fig_tendencia, use_container_width=True)
        
        with col2:
            st.markdown("### ⏰ Horários de Maior Incidência")
            
            # Gráfico de barras por hora
            horas_data = pd.DataFrame({
                'Hora': [f"{h:02d}:00" for h in range(24)],
                'Anomalias': np.random.randint(5, 50, size=24)
            })
            horas_data.loc[[2, 3, 4, 22, 23], 'Anomalias'] = horas_data.loc[[2, 3, 4, 22, 23], 'Anomalias'] * 3
            
            fig_horas = px.bar(horas_data, x='Hora', y='Anomalias',
                             title="Distribuição de Anomalias por Hora do Dia",
                             color='Anomalias',
                             color_continuous_scale='Reds')
            fig_horas.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_horas, use_container_width=True)
            
            st.warning("⚠️ Atenção: Picos de atividade suspeita detectados entre 02:00-04:00 e 22:00-23:00")
    
    with tab5:
        st.subheader("Plano de Ação e Recomendações")
        
        # Cards de ações prioritárias
        st.markdown("### 🎯 Ações Prioritárias")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: #FEE2E2; padding: 20px; border-radius: 12px; border: 1px solid #FECACA;">
                <h4 style="color: #991B1B; margin-bottom: 10px;">🚨 Urgente</h4>
                <ul style="color: #7F1D1D; margin: 0; padding-left: 20px;">
                    <li>Bloquear 23 pagamentos suspeitos</li>
                    <li>Auditar contratos do DNIT</li>
                    <li>Investigar rede de empresas #A0047</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #FEF3C7; padding: 20px; border-radius: 12px; border: 1px solid #FDE68A;">
                <h4 style="color: #92400E; margin-bottom: 10px;">⚡ Alta Prioridade</h4>
                <ul style="color: #78350F; margin: 0; padding-left: 20px;">
                    <li>Revisar processos de compra</li>
                    <li>Treinar equipe de compliance</li>
                    <li>Atualizar regras de detecção</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: #DBEAFE; padding: 20px; border-radius: 12px; border: 1px solid #BFDBFE;">
                <h4 style="color: #1E3A8A; margin-bottom: 10px;">📋 Médio Prazo</h4>
                <ul style="color: #1E40AF; margin: 0; padding-left: 20px;">
                    <li>Implementar novo sistema</li>
                    <li>Criar dashboard executivo</li>
                    <li>Estabelecer KPIs mensais</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Matriz de risco
        st.markdown("### 🎲 Matriz de Risco")
        
        # Criar dados para a matriz
        riscos_data = []
        for i in range(20):
            riscos_data.append({
                'Impacto': np.random.randint(1, 11),
                'Probabilidade': np.random.randint(1, 11),
                'Anomalia': f'Anomalia {i+1}',
                'Valor': np.random.randint(100000, 5000000)
            })
        
        df_riscos = pd.DataFrame(riscos_data)
        
        fig_matriz = px.scatter(df_riscos, x='Probabilidade', y='Impacto',
                               size='Valor', hover_data=['Anomalia', 'Valor'],
                               title="Matriz de Risco - Anomalias Detectadas",
                               labels={'Probabilidade': 'Probabilidade de Ocorrência',
                                      'Impacto': 'Impacto Financeiro'},
                               color='Valor',
                               color_continuous_scale='Reds')
        
        # Adicionar quadrantes
        fig_matriz.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5,
                            fillcolor="lightgreen", opacity=0.2, line_width=0)
        fig_matriz.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5,
                            fillcolor="yellow", opacity=0.2, line_width=0)
        fig_matriz.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10,
                            fillcolor="orange", opacity=0.2, line_width=0)
        fig_matriz.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10,
                            fillcolor="red", opacity=0.2, line_width=0)
        
        fig_matriz.update_layout(
            xaxis=dict(range=[0, 11]),
            yaxis=dict(range=[0, 11])
        )
        
        st.plotly_chart(fig_matriz, use_container_width=True)
        
        # Recomendações finais
        st.markdown("### 💡 Recomendações do Sistema")
        
        recomendacoes = [
            {
                "titulo": "Implementar Monitoramento 24/7",
                "descricao": "Sistema de alertas em tempo real para detecção imediata de anomalias",
                "impacto": "Redução de 70% no tempo de resposta",
                "prazo": "30 dias"
            },
            {
                "titulo": "Capacitação em Compliance",
                "descricao": "Programa de treinamento para todos os gestores de contratos",
                "impacto": "Prevenção de 40% das irregularidades",
                "prazo": "60 dias"
            },
            {
                "titulo": "Integração de Dados",
                "descricao": "Unificar bases de dados para análise cruzada automática",
                "impacto": "Aumento de 85% na detecção",
                "prazo": "90 dias"
            }
        ]
        
        for rec in recomendacoes:
            st.markdown(f"""
            <div style="background: white; padding: 20px; margin-bottom: 15px; 
                        border-radius: 12px; border: 1px solid #E5E7EB;">
                <h4 style="color: #047857; margin-bottom: 10px;">{rec['titulo']}</h4>
                <p style="color: #6B7280; margin-bottom: 10px;">{rec['descricao']}</p>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #3B82F6;"><strong>Impacto:</strong> {rec['impacto']}</span>
                    <span style="color: #F59E0B;"><strong>Prazo:</strong> {rec['prazo']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)