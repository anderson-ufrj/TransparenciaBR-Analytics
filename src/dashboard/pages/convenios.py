import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import json

# Page configuration
st.set_page_config(
    page_title="Convênios - TransparênciaBR Analytics",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Brazilian theme
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #009C3B 0%, #FFDF00 50%, #002776 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
        border-left: 4px solid #009C3B;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #002776;
    }
    .kpi-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .filter-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
    }
    .status-vigente {
        background-color: #28a745;
        color: white;
    }
    .status-finalizado {
        background-color: #6c757d;
        color: white;
    }
    .status-cancelado {
        background-color: #dc3545;
        color: white;
    }
    .status-suspenso {
        background-color: #ffc107;
        color: #212529;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .alert-critical {
        background-color: #fee;
        border-color: #dc3545;
        color: #721c24;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    .alert-info {
        background-color: #d1ecf1;
        border-color: #17a2b8;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🤝 Painel de Convênios</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Acompanhamento e análise de convênios federais</p>
    </div>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_convenios_data():
    np.random.seed(42)
    n_convenios = 500
    
    orgaos = [
        "Ministério da Saúde", "Ministério da Educação", "Ministério do Desenvolvimento Social",
        "Ministério da Infraestrutura", "Ministério do Meio Ambiente", "Ministério da Cultura",
        "Ministério do Esporte", "Ministério da Agricultura", "Ministério da Ciência e Tecnologia"
    ]
    
    estados = [
        "SP", "RJ", "MG", "BA", "PR", "RS", "PE", "CE", "PA", "MA",
        "GO", "SC", "PB", "RN", "ES", "AL", "PI", "MT", "MS", "SE",
        "RO", "TO", "AC", "AP", "RR", "AM", "DF"
    ]
    
    situacoes = ["Vigente", "Finalizado", "Cancelado", "Suspenso"]
    situacao_weights = [0.4, 0.3, 0.2, 0.1]
    
    tipos = [
        "Saúde", "Educação", "Infraestrutura", "Assistência Social",
        "Meio Ambiente", "Cultura", "Esporte", "Agricultura"
    ]
    
    data = []
    for i in range(n_convenios):
        inicio = datetime.now() - timedelta(days=np.random.randint(0, 1825))
        duracao = np.random.randint(180, 1095)
        fim = inicio + timedelta(days=duracao)
        
        valor_total = np.random.uniform(100000, 5000000)
        percentual_executado = np.random.uniform(0, 100) if np.random.random() > 0.3 else 0
        
        data.append({
            "numero": f"CV{2020 + i//100}{i:04d}",
            "orgao": np.random.choice(orgaos),
            "convenente": f"Prefeitura de {np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Curitiba', 'Fortaleza', 'Manaus', 'Brasília'])}",
            "objeto": f"Convênio para {np.random.choice(['construção', 'reforma', 'ampliação', 'manutenção', 'aquisição'])} de {np.random.choice(['hospital', 'escola', 'creche', 'unidade básica de saúde', 'centro comunitário', 'quadra esportiva'])}",
            "tipo": np.random.choice(tipos),
            "estado": np.random.choice(estados),
            "situacao": np.random.choices(situacoes, weights=situacao_weights)[0],
            "valor_total": valor_total,
            "valor_liberado": valor_total * percentual_executado / 100,
            "percentual_executado": percentual_executado,
            "data_inicio": inicio,
            "data_fim": fim,
            "prazo_prestacao": fim + timedelta(days=60),
            "ano": inicio.year
        })
    
    return pd.DataFrame(data)

# Load data
df_convenios = generate_convenios_data()

# Filters
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    orgao_filter = st.selectbox(
        "Órgão Concedente",
        ["Todos"] + sorted(df_convenios["orgao"].unique()),
        help="Selecione o órgão concedente"
    )

with col2:
    estado_filter = st.selectbox(
        "Estado",
        ["Todos"] + sorted(df_convenios["estado"].unique()),
        help="Selecione o estado"
    )

with col3:
    situacao_filter = st.selectbox(
        "Situação",
        ["Todas"] + sorted(df_convenios["situacao"].unique()),
        help="Selecione a situação do convênio"
    )

with col4:
    ano_filter = st.selectbox(
        "Ano",
        ["Todos"] + sorted(df_convenios["ano"].unique(), reverse=True),
        help="Selecione o ano de início"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
df_filtered = df_convenios.copy()
if orgao_filter != "Todos":
    df_filtered = df_filtered[df_filtered["orgao"] == orgao_filter]
if estado_filter != "Todos":
    df_filtered = df_filtered[df_filtered["estado"] == estado_filter]
if situacao_filter != "Todas":
    df_filtered = df_filtered[df_filtered["situacao"] == situacao_filter]
if ano_filter != "Todos":
    df_filtered = df_filtered[df_filtered["ano"] == int(ano_filter)]

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(df_filtered):,}</div>
            <div class="kpi-label">Total de Convênios</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    valor_total = df_filtered["valor_total"].sum()
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">R$ {valor_total/1e9:.1f}B</div>
            <div class="kpi-label">Valor Total</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    valor_liberado = df_filtered["valor_liberado"].sum()
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">R$ {valor_liberado/1e9:.1f}B</div>
            <div class="kpi-label">Valor Liberado</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    taxa_execucao = (valor_liberado / valor_total * 100) if valor_total > 0 else 0
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{taxa_execucao:.1f}%</div>
            <div class="kpi-label">Taxa de Execução</div>
        </div>
    """, unsafe_allow_html=True)

# Tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Linha do Tempo", 
    "🗺️ Distribuição Geográfica", 
    "💰 Análise Financeira",
    "📈 Monitoramento de Status",
    "📋 Detalhamento"
])

with tab1:
    st.subheader("Evolução Temporal dos Convênios")
    
    # Timeline chart
    df_timeline = df_filtered.groupby([pd.Grouper(key='data_inicio', freq='M'), 'situacao']).size().reset_index(name='count')
    
    fig_timeline = px.area(
        df_timeline,
        x='data_inicio',
        y='count',
        color='situacao',
        title='Número de Convênios por Mês',
        color_discrete_map={
            'Vigente': '#28a745',
            'Finalizado': '#6c757d',
            'Cancelado': '#dc3545',
            'Suspenso': '#ffc107'
        }
    )
    fig_timeline.update_layout(height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Value over time
    df_value_timeline = df_filtered.groupby(pd.Grouper(key='data_inicio', freq='Q')).agg({
        'valor_total': 'sum',
        'valor_liberado': 'sum'
    }).reset_index()
    
    fig_values = go.Figure()
    fig_values.add_trace(go.Scatter(
        x=df_value_timeline['data_inicio'],
        y=df_value_timeline['valor_total'],
        name='Valor Total',
        line=dict(color='#002776', width=3)
    ))
    fig_values.add_trace(go.Scatter(
        x=df_value_timeline['data_inicio'],
        y=df_value_timeline['valor_liberado'],
        name='Valor Liberado',
        line=dict(color='#009C3B', width=3)
    ))
    fig_values.update_layout(
        title='Evolução dos Valores (Trimestral)',
        yaxis_title='Valor (R$)',
        height=400
    )
    st.plotly_chart(fig_values, use_container_width=True)

with tab2:
    st.subheader("Distribuição Geográfica dos Convênios")
    
    # Map data preparation
    df_geo = df_filtered.groupby('estado').agg({
        'valor_total': 'sum',
        'numero': 'count',
        'valor_liberado': 'sum'
    }).reset_index()
    df_geo.columns = ['estado', 'valor_total', 'quantidade', 'valor_liberado']
    
    # Create choropleth map
    fig_map = px.choropleth(
        df_geo,
        locations='estado',
        locationmode='geojson-id',
        color='valor_total',
        hover_data=['quantidade', 'valor_liberado'],
        color_continuous_scale='YlOrRd',
        title='Valor Total de Convênios por Estado'
    )
    
    # Update map layout
    fig_map.update_geos(
        visible=False,
        resolution=50,
        showcountries=True,
        countrycolor="RebeccaPurple",
        showcoastlines=True,
        coastlinecolor="RebeccaPurple",
        showland=True,
        landcolor='LightGray',
        center={"lat": -15.7801, "lon": -47.9292},
        projection_scale=3
    )
    fig_map.update_layout(height=500)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Bar chart by state
    fig_bar_estado = px.bar(
        df_geo.sort_values('valor_total', ascending=True).tail(15),
        x='valor_total',
        y='estado',
        orientation='h',
        title='Top 15 Estados por Valor Total',
        color='valor_total',
        color_continuous_scale='Blues'
    )
    fig_bar_estado.update_layout(height=400)
    st.plotly_chart(fig_bar_estado, use_container_width=True)

with tab3:
    st.subheader("Análise Financeira dos Convênios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart by type
        df_tipo = df_filtered.groupby('tipo')['valor_total'].sum().reset_index()
        fig_pie = px.pie(
            df_tipo,
            values='valor_total',
            names='tipo',
            title='Distribuição por Tipo de Convênio',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Execution rate by organ
        df_execucao = df_filtered.groupby('orgao').agg({
            'valor_total': 'sum',
            'valor_liberado': 'sum'
        }).reset_index()
        df_execucao['taxa_execucao'] = (df_execucao['valor_liberado'] / df_execucao['valor_total'] * 100).round(1)
        
        fig_exec = px.bar(
            df_execucao.sort_values('taxa_execucao', ascending=True),
            x='taxa_execucao',
            y='orgao',
            orientation='h',
            title='Taxa de Execução por Órgão (%)',
            color='taxa_execucao',
            color_continuous_scale='RdYlGn'
        )
        fig_exec.update_layout(height=400)
        st.plotly_chart(fig_exec, use_container_width=True)
    
    # Financial metrics table
    st.subheader("Métricas Financeiras por Órgão")
    df_metricas = df_filtered.groupby('orgao').agg({
        'valor_total': ['sum', 'mean', 'count'],
        'valor_liberado': 'sum',
        'percentual_executado': 'mean'
    }).round(2)
    df_metricas.columns = ['Valor Total', 'Valor Médio', 'Qtd Convênios', 'Valor Liberado', 'Execução Média (%)']
    df_metricas = df_metricas.sort_values('Valor Total', ascending=False)
    
    st.dataframe(
        df_metricas.style.format({
            'Valor Total': 'R$ {:,.2f}',
            'Valor Médio': 'R$ {:,.2f}',
            'Valor Liberado': 'R$ {:,.2f}',
            'Execução Média (%)': '{:.1f}%'
        }),
        use_container_width=True
    )

with tab4:
    st.subheader("Monitoramento de Status dos Convênios")
    
    # Status distribution
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sunburst chart
        df_sunburst = df_filtered.groupby(['situacao', 'tipo']).size().reset_index(name='count')
        fig_sunburst = px.sunburst(
            df_sunburst,
            path=['situacao', 'tipo'],
            values='count',
            title='Distribuição Hierárquica por Status e Tipo',
            color_discrete_map={
                'Vigente': '#28a745',
                'Finalizado': '#6c757d',
                'Cancelado': '#dc3545',
                'Suspenso': '#ffc107'
            }
        )
        fig_sunburst.update_layout(height=400)
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    with col2:
        # Status summary
        st.markdown("### Resumo por Status")
        for status in df_filtered['situacao'].unique():
            count = len(df_filtered[df_filtered['situacao'] == status])
            percentage = (count / len(df_filtered) * 100)
            
            status_class = status.lower().replace(' ', '-')
            st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <span class="status-badge status-{status_class}">{status}</span>
                    <div style="margin-top: 0.5rem;">
                        <strong>{count}</strong> convênios ({percentage:.1f}%)
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Critical dates monitoring
    st.subheader("Monitoramento de Prazos Críticos")
    
    today = datetime.now()
    df_prazos = df_filtered[df_filtered['situacao'] == 'Vigente'].copy()
    df_prazos['dias_para_fim'] = (df_prazos['data_fim'] - today).dt.days
    df_prazos['dias_para_prestacao'] = (df_prazos['prazo_prestacao'] - today).dt.days
    
    # Convênios próximos ao vencimento
    df_vencendo = df_prazos[df_prazos['dias_para_fim'] <= 90].sort_values('dias_para_fim')
    
    if len(df_vencendo) > 0:
        st.markdown("""
            <div class="alert-box alert-warning">
                <strong>⚠️ Atenção:</strong> {} convênios vencem nos próximos 90 dias
            </div>
        """.format(len(df_vencendo)), unsafe_allow_html=True)
        
        st.dataframe(
            df_vencendo[['numero', 'convenente', 'valor_total', 'dias_para_fim']].head(10),
            use_container_width=True
        )

with tab5:
    st.subheader("Detalhamento dos Convênios")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Buscar convênio", placeholder="Digite número, órgão ou convenente...")
    with col2:
        items_per_page = st.selectbox("Itens por página", [10, 25, 50, 100], index=1)
    
    # Apply search
    df_detail = df_filtered.copy()
    if search_term:
        mask = (
            df_detail['numero'].str.contains(search_term, case=False, na=False) |
            df_detail['orgao'].str.contains(search_term, case=False, na=False) |
            df_detail['convenente'].str.contains(search_term, case=False, na=False) |
            df_detail['objeto'].str.contains(search_term, case=False, na=False)
        )
        df_detail = df_detail[mask]
    
    # Display table with pagination
    total_items = len(df_detail)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    if total_pages > 1:
        page = st.number_input(
            f"Página (1-{total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1
        )
    else:
        page = 1
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    
    # Format the display dataframe
    df_display = df_detail.iloc[start_idx:end_idx][
        ['numero', 'orgao', 'convenente', 'objeto', 'tipo', 'estado', 
         'situacao', 'valor_total', 'valor_liberado', 'percentual_executado', 
         'data_inicio', 'data_fim']
    ].copy()
    
    # Apply formatting
    df_display['valor_total'] = df_display['valor_total'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['valor_liberado'] = df_display['valor_liberado'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['percentual_executado'] = df_display['percentual_executado'].apply(lambda x: f"{x:.1f}%")
    df_display['data_inicio'] = df_display['data_inicio'].dt.strftime('%d/%m/%Y')
    df_display['data_fim'] = df_display['data_fim'].dt.strftime('%d/%m/%Y')
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    st.info(f"Mostrando {start_idx + 1} a {min(end_idx, total_items)} de {total_items} convênios")

# Alerts Section
st.markdown("---")
st.subheader("🚨 Alertas e Notificações")

col1, col2, col3 = st.columns(3)

with col1:
    convenios_criticos = len(df_filtered[
        (df_filtered['situacao'] == 'Vigente') & 
        (df_filtered['percentual_executado'] < 30) &
        ((df_filtered['data_fim'] - datetime.now()).dt.days < 180)
    ])
    if convenios_criticos > 0:
        st.markdown(f"""
            <div class="alert-box alert-critical">
                <strong>🔴 Crítico:</strong><br>
                {convenios_criticos} convênios com baixa execução e prazo curto
            </div>
        """, unsafe_allow_html=True)

with col2:
    prestacao_pendente = len(df_filtered[
        (df_filtered['situacao'] == 'Finalizado') &
        ((datetime.now() - df_filtered['data_fim']).dt.days > 60)
    ])
    if prestacao_pendente > 0:
        st.markdown(f"""
            <div class="alert-box alert-warning">
                <strong>⚠️ Atenção:</strong><br>
                {prestacao_pendente} convênios aguardando prestação de contas
            </div>
        """, unsafe_allow_html=True)

with col3:
    novos_convenios = len(df_filtered[
        (df_filtered['data_inicio'] >= datetime.now() - timedelta(days=30))
    ])
    st.markdown(f"""
        <div class="alert-box alert-info">
            <strong>ℹ️ Informação:</strong><br>
            {novos_convenios} novos convênios nos últimos 30 dias
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>TransparênciaBR Analytics - Dados de Convênios Federais</p>
        <p>Última atualização: {}</p>
    </div>
""".format(datetime.now().strftime("%d/%m/%Y às %H:%M")), unsafe_allow_html=True)