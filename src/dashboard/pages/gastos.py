"""
Página de análise de gastos com visualizações interativas.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_gastos_page():
    """Renderiza a página de análise de gastos."""
    
    st.markdown("## 📈 Análise de Gastos Públicos")
    st.markdown("Explore e analise os gastos do governo federal com visualizações interativas.")
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ano = st.selectbox(
            "Ano",
            options=[2024, 2023, 2022, 2021, 2020],
            index=0
        )
    
    with col2:
        mes = st.selectbox(
            "Mês",
            options=["Todos"] + [f"{i:02d}" for i in range(1, 13)],
            index=0
        )
    
    with col3:
        tipo_despesa = st.selectbox(
            "Tipo de Despesa",
            options=["Todas", "Pessoal", "Custeio", "Investimento", "Inversões"],
            index=0
        )
    
    with col4:
        orgao_filter = st.text_input("Filtrar por Órgão", placeholder="Digite o nome...")
    
    st.markdown("---")
    
    # KPIs
    st.markdown("### 💰 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Gasto",
            f"R$ {45.8:.1f} Bi",
            f"↑ {12.3:.1f}% vs ano anterior"
        )
    
    with col2:
        st.metric(
            "Média Mensal",
            f"R$ {3.82:.2f} Bi",
            f"↑ {8.5:.1f}% vs mês anterior"
        )
    
    with col3:
        st.metric(
            "Maior Gasto",
            "Min. Saúde",
            "R$ 12.4 Bi"
        )
    
    with col4:
        st.metric(
            "Execução Orçamentária",
            "87.3%",
            "↑ 2.1% vs meta"
        )
    
    st.markdown("---")
    
    # Visualizações principais
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Por Órgão", "📅 Temporal", "🗂️ Por Categoria", "🗺️ Geográfico"])
    
    with tab1:
        render_gastos_por_orgao()
    
    with tab2:
        render_analise_temporal()
    
    with tab3:
        render_gastos_por_categoria()
    
    with tab4:
        render_mapa_gastos()

def render_gastos_por_orgao():
    """Renderiza análise de gastos por órgão."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de barras horizontais
        orgaos = [
            "Ministério da Saúde",
            "Ministério da Educação", 
            "Ministério da Defesa",
            "Ministério da Infraestrutura",
            "Ministério do Desenvolvimento Social",
            "Ministério da Economia",
            "Ministério da Justiça",
            "Ministério da Agricultura",
            "Ministério do Meio Ambiente",
            "Outros"
        ]
        
        valores = [125.4, 98.7, 76.3, 54.2, 43.1, 38.9, 28.7, 24.3, 18.9, 67.5]
        
        df = pd.DataFrame({
            'Órgão': orgaos,
            'Valor (Bilhões)': valores
        })
        
        fig = px.bar(
            df.sort_values('Valor (Bilhões)'),
            x='Valor (Bilhões)',
            y='Órgão',
            orientation='h',
            title="Top 10 Órgãos por Volume de Gastos",
            color='Valor (Bilhões)',
            color_continuous_scale='Viridis',
            text='Valor (Bilhões)'
        )
        
        fig.update_traces(texttemplate='R$ %{text:.1f}B', textposition='outside')
        fig.update_layout(
            height=500,
            showlegend=False,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Estatísticas do órgão selecionado
        st.markdown("#### 📊 Detalhes do Órgão")
        
        orgao_selecionado = st.selectbox(
            "Selecione um órgão",
            options=orgaos,
            label_visibility="collapsed"
        )
        
        # Métricas do órgão
        st.metric("Total Gasto", f"R$ {125.4:.1f} Bi")
        st.metric("Variação Anual", "↑ 15.3%", delta_color="normal")
        st.metric("% do Total", "27.4%")
        st.metric("Contratos Ativos", "1.234")
        
        # Mini gráfico de evolução
        st.markdown("##### Evolução Mensal")
        meses = list(range(1, 13))
        valores_mensais = np.random.uniform(8, 12, 12)
        
        fig_mini = go.Figure()
        fig_mini.add_trace(go.Scatter(
            x=meses,
            y=valores_mensais,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig_mini.update_layout(
            height=200,
            margin=dict(t=10, b=0, l=0, r=0),
            showlegend=False,
            xaxis=dict(title="Mês"),
            yaxis=dict(title="Bilhões (R$)")
        )
        
        st.plotly_chart(fig_mini, use_container_width=True)

def render_analise_temporal():
    """Renderiza análise temporal dos gastos."""
    
    # Seletor de período
    col1, col2 = st.columns([3, 1])
    
    with col1:
        periodo = st.radio(
            "Período de Análise",
            options=["Últimos 12 meses", "Último ano", "Últimos 5 anos"],
            horizontal=True
        )
    
    with col2:
        tipo_grafico = st.selectbox(
            "Tipo de Gráfico",
            options=["Linha", "Área", "Barras"]
        )
    
    # Gerar dados de exemplo
    if periodo == "Últimos 12 meses":
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        valores = np.random.uniform(40, 60, 12)
    elif periodo == "Último ano":
        dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
        valores = np.random.uniform(1, 3, 365)
    else:
        dates = pd.date_range(end=datetime.now(), periods=60, freq='M')
        valores = np.random.uniform(35, 65, 60)
    
    df_temporal = pd.DataFrame({
        'Data': dates,
        'Valor': valores
    })
    
    # Criar gráfico baseado no tipo selecionado
    if tipo_grafico == "Linha":
        fig = px.line(
            df_temporal,
            x='Data',
            y='Valor',
            title="Evolução dos Gastos ao Longo do Tempo"
        )
    elif tipo_grafico == "Área":
        fig = px.area(
            df_temporal,
            x='Data',
            y='Valor',
            title="Evolução dos Gastos ao Longo do Tempo"
        )
    else:
        fig = px.bar(
            df_temporal,
            x='Data',
            y='Valor',
            title="Evolução dos Gastos ao Longo do Tempo"
        )
    
    fig.update_layout(
        height=400,
        xaxis_title="",
        yaxis_title="Valor (Bilhões R$)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de tendência
    st.markdown("#### 📈 Análise de Tendência")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Tendência**: Crescente")
        st.caption("Taxa de crescimento: 2.3% ao mês")
    
    with col2:
        st.warning("**Sazonalidade**: Alta em Dezembro")
        st.caption("Pico médio: 18% acima da média")
    
    with col3:
        st.success("**Previsão**: R$ 58.2 Bi")
        st.caption("Próximo mês (95% confiança)")

def render_gastos_por_categoria():
    """Renderiza gastos por categoria."""
    
    # Gráficos de composição
    col1, col2 = st.columns(2)
    
    with col1:
        # Donut chart por tipo de despesa
        categorias = ["Pessoal", "Custeio", "Investimento", "Inversões", "Amortização"]
        valores = [234.5, 123.4, 45.6, 23.4, 12.3]
        
        fig = go.Figure(data=[go.Pie(
            labels=categorias,
            values=valores,
            hole=.4
        )])
        
        fig.update_layout(
            title="Distribuição por Tipo de Despesa",
            height=400,
            annotations=[dict(text='2024', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Treemap por função
        funcoes = ["Saúde", "Educação", "Previdência", "Defesa", "Assistência", "Transporte"]
        valores_funcao = [125, 98, 87, 76, 54, 43]
        
        fig = px.treemap(
            names=funcoes,
            parents=[""] * len(funcoes),
            values=valores_funcao,
            title="Gastos por Função de Governo"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela detalhada
    st.markdown("#### 📋 Detalhamento por Categoria")
    
    df_detalhes = pd.DataFrame({
        'Categoria': categorias * 2,
        'Subcategoria': ['Ativos', 'Inativos', 'Material', 'Serviços', 'Obras', 'Equipamentos', 
                        'Financeiras', 'Imobiliárias', 'Dívida Interna', 'Dívida Externa'],
        'Valor (Mi)': np.random.uniform(1000, 50000, 10),
        'Execução (%)': np.random.uniform(70, 100, 10),
        'Variação (%)': np.random.uniform(-10, 20, 10)
    })
    
    st.dataframe(
        df_detalhes.style.format({
            'Valor (Mi)': 'R$ {:,.0f}',
            'Execução (%)': '{:.1f}%',
            'Variação (%)': '{:+.1f}%'
        }).background_gradient(subset=['Execução (%)']),
        use_container_width=True,
        hide_index=True
    )

def render_mapa_gastos():
    """Renderiza mapa de gastos por região."""
    
    st.markdown("#### 🗺️ Distribuição Geográfica dos Gastos")
    
    # Dados por estado (mockados)
    estados_br = {
        'Estado': ['SP', 'RJ', 'MG', 'BA', 'PR', 'RS', 'PE', 'CE', 'PA', 'MA'],
        'Valor': [45.6, 32.4, 28.9, 21.3, 18.7, 17.5, 15.4, 13.2, 11.8, 9.7],
        'Per Capita': [989, 1876, 1367, 1432, 1654, 1543, 1621, 1456, 1378, 1402]
    }
    
    df_estados = pd.DataFrame(estados_br)
    
    # Visualização
    view_type = st.radio(
        "Visualizar por:",
        options=["Valor Total", "Per Capita"],
        horizontal=True
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de barras por estado
        y_col = 'Valor' if view_type == "Valor Total" else 'Per Capita'
        y_title = 'Bilhões (R$)' if view_type == "Valor Total" else 'R$ per capita'
        
        fig = px.bar(
            df_estados.sort_values(y_col, ascending=True),
            x=y_col,
            y='Estado',
            orientation='h',
            title=f"Gastos por Estado - {view_type}",
            color=y_col,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title=y_title
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Estatísticas regionais
        st.markdown("##### 📊 Resumo Regional")
        
        regioes = {
            'Sudeste': 107.9,
            'Nordeste': 78.4,
            'Sul': 53.7,
            'Norte': 32.8,
            'Centro-Oeste': 24.6
        }
        
        for regiao, valor in regioes.items():
            st.metric(regiao, f"R$ {valor:.1f} Bi")
    
    # Insights
    st.info("💡 **Insight**: A região Sudeste concentra 36% dos gastos totais, mas tem o 3º maior gasto per capita.")