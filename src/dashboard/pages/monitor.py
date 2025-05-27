"""
Página de monitoramento da coleta de dados.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import json

def render_monitor_page():
    """Renderiza a página de monitoramento."""
    
    st.markdown("## 📊 Monitor de Coleta de Dados")
    st.markdown("Acompanhe em tempo real o status das coletas e a saúde do sistema.")
    
    # Status geral
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API Status", "🟢 Online", "Latência: 235ms")
    
    with col2:
        st.metric("Taxa de Sucesso", "98.5%", "↑ 0.3%")
    
    with col3:
        st.metric("Dados Coletados Hoje", "45.2K", "↑ 12% vs ontem")
    
    with col4:
        st.metric("Próxima Coleta", "15:30", "em 2h 15min")
    
    st.markdown("---")
    
    # Gráfico de coletas em tempo real
    st.markdown("### 📈 Coletas nas Últimas 24 Horas")
    
    # Dados simulados
    hours = list(range(24))
    current_hour = datetime.now().hour
    
    # Simular dados de coleta por hora
    coletas_sucesso = [int(1000 + 500 * abs(h - 12) / 12 + 200 * (0.5 - abs(h - current_hour) / 24)) for h in hours]
    coletas_erro = [int(50 + 30 * (0.5 - abs(h - 12) / 24)) for h in hours]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Sucesso',
        x=hours,
        y=coletas_sucesso,
        marker_color='green'
    ))
    
    fig.add_trace(go.Bar(
        name='Erro',
        x=hours,
        y=coletas_erro,
        marker_color='red'
    ))
    
    fig.update_layout(
        barmode='stack',
        title="",
        xaxis_title="Hora do Dia",
        yaxis_title="Número de Requisições",
        height=300,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de endpoints
    st.markdown("### 📋 Status por Endpoint")
    
    endpoints_data = {
        'Endpoint': [
            'contratos',
            'pagamentos',
            'licitacoes',
            'fornecedores',
            'servidores',
            'convenios',
            'empenhos'
        ],
        'Status': ['🟢', '🟢', '🟡', '🟢', '🔴', '🟢', '🟢'],
        'Última Coleta': [
            'Há 5 min',
            'Há 12 min',
            'Há 1h',
            'Há 30 min',
            'Há 2 dias',
            'Há 45 min',
            'Há 20 min'
        ],
        'Registros/h': [2500, 8900, 450, 1200, 0, 780, 3400],
        'Taxa Sucesso': ['99.8%', '99.5%', '95.2%', '98.7%', '0%', '97.3%', '99.1%'],
        'Tempo Médio': ['1.2s', '2.3s', '5.4s', '1.8s', '-', '3.2s', '1.5s']
    }
    
    df_endpoints = pd.DataFrame(endpoints_data)
    
    st.dataframe(
        df_endpoints,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Registros/h": st.column_config.NumberColumn("Registros/h", format="%d"),
        }
    )
    
    # Logs em tempo real
    st.markdown("### 📜 Logs Recentes")
    
    # Container para logs com altura fixa
    log_container = st.container()
    
    with log_container:
        logs = [
            {"time": "14:23:45", "level": "INFO", "message": "Coleta iniciada: contratos (página 145/200)"},
            {"time": "14:23:32", "level": "SUCCESS", "message": "1.234 pagamentos processados com sucesso"},
            {"time": "14:23:15", "level": "WARNING", "message": "Rate limit próximo: 28/30 requisições"},
            {"time": "14:22:58", "level": "ERROR", "message": "Timeout ao conectar com endpoint servidores"},
            {"time": "14:22:45", "level": "INFO", "message": "Cache hit: fornecedores (economia de 2.3s)"},
            {"time": "14:22:30", "level": "SUCCESS", "message": "Backup automático concluído"},
        ]
        
        for log in logs:
            if log["level"] == "ERROR":
                st.error(f"**{log['time']}** - {log['message']}")
            elif log["level"] == "WARNING":
                st.warning(f"**{log['time']}** - {log['message']}")
            elif log["level"] == "SUCCESS":
                st.success(f"**{log['time']}** - {log['message']}")
            else:
                st.info(f"**{log['time']}** - {log['message']}")
    
    # Controles
    st.markdown("### ⚙️ Controles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Iniciar Coleta Manual", type="primary", use_container_width=True):
            st.success("Coleta manual iniciada!")
    
    with col2:
        if st.button("⏸️ Pausar Todas as Coletas", use_container_width=True):
            st.warning("Coletas pausadas")
    
    with col3:
        if st.button("🔄 Reiniciar Sistema", use_container_width=True):
            st.info("Reiniciando sistema...")