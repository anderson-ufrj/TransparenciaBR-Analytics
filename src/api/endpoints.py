"""
Construtor de endpoints para a API do Portal da Transparência.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode

from config.constants import ENDPOINTS


class EndpointBuilder:
    """Constrói URLs e parâmetros para endpoints da API."""
    
    @staticmethod
    def build_url(base_url: str, endpoint: str, params: Optional[Dict] = None) -> str:
        """
        Constrói URL completa com parâmetros.
        
        Args:
            base_url: URL base da API
            endpoint: Endpoint específico
            params: Parâmetros da query
            
        Returns:
            URL completa formatada
        """
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        if params:
            # Remove valores None e converte para string
            clean_params = {
                k: str(v) for k, v in params.items() 
                if v is not None
            }
            if clean_params:
                url += f"?{urlencode(clean_params)}"
                
        return url
    
    @staticmethod
    def get_gastos_params(
        codigo_orgao: Optional[str] = None,
        ano: Optional[int] = None,
        mes: Optional[int] = None,
        pagina: int = 1,
        quantidade_registros: int = 500
    ) -> Dict:
        """Parâmetros para endpoint de gastos por órgão."""
        params = {
            "pagina": pagina,
            "quantidadeRegistros": quantidade_registros
        }
        
        if codigo_orgao:
            params["codigoOrgao"] = codigo_orgao
        if ano:
            params["ano"] = ano
        if mes:
            params["mes"] = mes
            
        return params
    
    @staticmethod
    def get_contratos_params(
        data_inicial: Optional[str] = None,
        data_final: Optional[str] = None,
        codigo_orgao: Optional[str] = None,
        cnpj_cpf_fornecedor: Optional[str] = None,
        pagina: int = 1,
        quantidade_registros: int = 500
    ) -> Dict:
        """Parâmetros para endpoint de contratos."""
        params = {
            "pagina": pagina,
            "quantidadeRegistros": quantidade_registros
        }
        
        if data_inicial:
            params["dataInicial"] = data_inicial
        if data_final:
            params["dataFinal"] = data_final
        if codigo_orgao:
            params["codigoOrgao"] = codigo_orgao
        if cnpj_cpf_fornecedor:
            params["cnpjCpfFornecedor"] = cnpj_cpf_fornecedor
            
        return params
    
    @staticmethod
    def get_licitacoes_params(
        data_inicial: Optional[str] = None,
        data_final: Optional[str] = None,
        codigo_orgao: Optional[str] = None,
        modalidade: Optional[str] = None,
        situacao: Optional[str] = None,
        pagina: int = 1,
        quantidade_registros: int = 500
    ) -> Dict:
        """Parâmetros para endpoint de licitações."""
        params = {
            "pagina": pagina,
            "quantidadeRegistros": quantidade_registros
        }
        
        if data_inicial:
            params["dataInicial"] = data_inicial
        if data_final:
            params["dataFinal"] = data_final
        if codigo_orgao:
            params["codigoOrgao"] = codigo_orgao
        if modalidade:
            params["codigoModalidadeCompra"] = modalidade
        if situacao:
            params["codigoSituacao"] = situacao
            
        return params
    
    @staticmethod
    def get_servidores_params(
        orgao_exercicio: Optional[str] = None,
        orgao_lotacao: Optional[str] = None,
        tipo_servidor: Optional[int] = None,
        pagina: int = 1,
        quantidade_registros: int = 500
    ) -> Dict:
        """Parâmetros para endpoint de servidores."""
        params = {
            "pagina": pagina,
            "quantidadeRegistros": quantidade_registros
        }
        
        if orgao_exercicio:
            params["orgaoExercicio"] = orgao_exercicio
        if orgao_lotacao:
            params["orgaoLotacao"] = orgao_lotacao
        if tipo_servidor:
            params["tipoServidor"] = tipo_servidor
            
        return params
    
    @staticmethod
    def get_cartoes_params(
        data_transacao_inicio: Optional[str] = None,
        data_transacao_fim: Optional[str] = None,
        codigo_orgao: Optional[str] = None,
        cpf_portador: Optional[str] = None,
        cnpj_cpf_favorecido: Optional[str] = None,
        pagina: int = 1,
        quantidade_registros: int = 500
    ) -> Dict:
        """Parâmetros para endpoint de cartões de pagamento."""
        params = {
            "pagina": pagina,
            "quantidadeRegistros": quantidade_registros
        }
        
        if data_transacao_inicio:
            params["dataTransacaoInicio"] = data_transacao_inicio
        if data_transacao_fim:
            params["dataTransacaoFim"] = data_transacao_fim
        if codigo_orgao:
            params["codigoOrgao"] = codigo_orgao
        if cpf_portador:
            params["cpfPortador"] = cpf_portador
        if cnpj_cpf_favorecido:
            params["cnpjCpfFavorecido"] = cnpj_cpf_favorecido
            
        return params
    
    @staticmethod
    def format_date(date: Union[str, datetime]) -> str:
        """
        Formata data para o padrão da API (dd/mm/yyyy).
        
        Args:
            date: Data como string ou datetime
            
        Returns:
            Data formatada como string
        """
        if isinstance(date, datetime):
            return date.strftime("%d/%m/%Y")
        return date
    
    @staticmethod
    def validate_cpf_cnpj(doc: str) -> str:
        """
        Valida e formata CPF/CNPJ removendo caracteres especiais.
        
        Args:
            doc: CPF ou CNPJ
            
        Returns:
            Documento formatado apenas com números
        """
        return ''.join(filter(str.isdigit, doc))