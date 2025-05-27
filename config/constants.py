"""
Constantes utilizadas em todo o projeto.
"""

from datetime import datetime

# Endpoints da API
ENDPOINTS = {
    "gastos": "/despesas/por-orgao",
    "contratos": "/contratos",
    "servidores": "/servidores",
    "licitacoes": "/licitacoes",
    "cartoes": "/cartoes",
    "orgaos": "/orgaos-siafi",
    "convenios": "/convenios",
    "transferencias": "/transferencias",
    "empresas": "/fornecedores",
    "pessoas": "/pessoas-fisicas",
    "beneficios": "/beneficios-cidadao",
    "cpgf": "/cartoes-pagamento",
    "sancoes": "/sancoes"
}

# Modalidades de licitação
MODALIDADES_LICITACAO = {
    "1": "Convite",
    "2": "Tomada de Preços",
    "3": "Concorrência",
    "4": "Concorrência Internacional",
    "5": "Pregão",
    "6": "Pregão Eletrônico",
    "7": "Dispensa de Licitação",
    "8": "Inexigibilidade",
    "9": "Consulta",
    "10": "Concurso",
    "11": "Leilão",
    "12": "Chamamento Público",
    "13": "Regime Diferenciado de Contratação"
}

# Situações de contratos
SITUACOES_CONTRATO = {
    "01": "Ativo",
    "02": "Concluído",
    "03": "Rescindido",
    "04": "Suspenso",
    "05": "Cancelado",
    "06": "Em Execução",
    "07": "Paralisado"
}

# Tipos de despesa
TIPOS_DESPESA = {
    "1": "Pessoal e Encargos Sociais",
    "2": "Juros e Encargos da Dívida",
    "3": "Outras Despesas Correntes",
    "4": "Investimentos",
    "5": "Inversões Financeiras",
    "6": "Amortização da Dívida"
}

# Fases da despesa
FASES_DESPESA = {
    "EMP": "Empenho",
    "LIQ": "Liquidação",
    "PAG": "Pagamento",
    "RPP": "Restos a Pagar Processados",
    "RPNP": "Restos a Pagar Não Processados"
}

# Órgãos principais (top 20 por orçamento)
ORGAOS_PRINCIPAIS = {
    "25000": "Ministério da Economia",
    "26000": "Ministério da Educação",
    "36000": "Ministério da Saúde",
    "52000": "Ministério da Defesa",
    "55000": "Ministério da Cidadania",
    "22000": "Ministério da Agricultura",
    "35000": "Ministério das Relações Exteriores",
    "54000": "Ministério do Turismo",
    "44000": "Ministério do Meio Ambiente",
    "37000": "Ministério da Justiça e Segurança Pública",
    "42000": "Ministério da Cultura",
    "39000": "Ministério da Infraestrutura",
    "41000": "Ministério das Comunicações",
    "53000": "Ministério do Desenvolvimento Regional",
    "24000": "Ministério da Ciência, Tecnologia e Inovações",
    "30000": "Ministério da Previdência Social",
    "38000": "Ministério do Trabalho e Emprego",
    "56000": "Ministério das Cidades",
    "28000": "Ministério do Desenvolvimento e Assistência Social",
    "51000": "Ministério do Esporte"
}

# Estados brasileiros
ESTADOS_BR = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}

# Limites de análise
MAX_RECORDS_PER_REQUEST = 1000
DEFAULT_PAGE_SIZE = 500
MAX_PARALLEL_REQUESTS = 5
CACHE_DEFAULT_TTL = 86400  # 24 horas em segundos

# Datas padrão para análise
DEFAULT_START_DATE = datetime(2023, 1, 1)
DEFAULT_END_DATE = datetime(2024, 12, 31)

# Thresholds para detecção de anomalias
ANOMALY_Z_SCORE_THRESHOLD = 3.0
ANOMALY_IQR_MULTIPLIER = 1.5
MIN_SAMPLES_FOR_ANOMALY = 30

# Configurações de visualização
PLOT_DEFAULT_WIDTH = 1200
PLOT_DEFAULT_HEIGHT = 600
COLOR_PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

# Formatos de data
DATE_FORMAT_API = "%Y-%m-%d"
DATE_FORMAT_BR = "%d/%m/%Y"
DATETIME_FORMAT_BR = "%d/%m/%Y %H:%M:%S"