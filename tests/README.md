# Tests

Este diretório contém os testes automatizados do projeto TransparenciaBR-Analytics.

## Estrutura

- `test_client.py` - Testes unitários do cliente API (com mocks)
- `test_api_connection.py` - Testes de integração com a API real

## Executando os Testes

### Testes Unitários (sem API)
```bash
pytest tests/test_client.py -v
```

### Testes de Integração (requer credenciais)
```bash
pytest tests/test_api_connection.py -v
```

### Todos os Testes com Cobertura
```bash
pytest tests/ -v --cov=src --cov-report=html
```

## CI/CD

No GitHub Actions, apenas os testes unitários são executados para evitar dependência de credenciais da API.