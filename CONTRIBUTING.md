# Guia de Contribuição 🤝

Obrigado por considerar contribuir com o TransparenciaBR-Analytics! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Como Contribuir

### 1. Reportando Bugs
- Use a seção [Issues](https://github.com/anderson-ufrj/TransparenciaBR-Analytics/issues)
- Descreva o bug claramente
- Inclua passos para reproduzir
- Adicione screenshots se aplicável

### 2. Sugerindo Melhorias
- Abra uma [Issue](https://github.com/anderson-ufrj/TransparenciaBR-Analytics/issues) com tag "enhancement"
- Explique a melhoria proposta
- Forneça exemplos de uso

### 3. Enviando Pull Requests

#### Setup do Ambiente
```bash
# Fork o repositório
# Clone seu fork
git clone https://github.com/seu-usuario/TransparenciaBR-Analytics.git
cd TransparenciaBR-Analytics

# Adicione o upstream
git remote add upstream https://github.com/anderson-ufrj/TransparenciaBR-Analytics.git

# Crie um branch para sua feature
git checkout -b feature/minha-feature
```

#### Desenvolvimento
```bash
# Instale as dependências
pip install -r requirements.txt

# Execute os testes
pytest tests/

# Formate o código
black src/ tests/
isort src/ tests/
```

#### Commits
Use commits semânticos em português:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `test:` testes
- `refactor:` refatoração
- `chore:` tarefas gerais

Exemplos:
```bash
git commit -m "feat: adicionar análise de gastos por órgão"
git commit -m "fix: corrigir erro no parser de datas"
git commit -m "docs: atualizar exemplos no README"
```

#### Pull Request
1. Atualize seu branch com o main
```bash
git fetch upstream
git rebase upstream/main
```

2. Push para seu fork
```bash
git push origin feature/minha-feature
```

3. Abra um Pull Request
- Descreva as mudanças
- Referencie issues relacionadas
- Adicione screenshots se aplicável

## 🧪 Padrões de Código

### Python
- Use type hints
- Docstrings em Google Style
- Máximo 100 caracteres por linha
- Classes em PascalCase
- Funções em snake_case

### Exemplo:
```python
def processar_dados(df: pd.DataFrame, tipo: str) -> pd.DataFrame:
    """
    Processa dados do Portal da Transparência.
    
    Args:
        df: DataFrame com dados brutos
        tipo: Tipo de processamento ('contratos', 'pagamentos')
        
    Returns:
        DataFrame processado
    """
    # Implementação
    return df
```

## 📁 Estrutura de Arquivos

- `/src` - Código fonte principal
- `/tests` - Testes automatizados
- `/notebooks` - Análises exploratórias
- `/docs` - Documentação
- `/data` - Dados (não commitar dados sensíveis!)

## ✅ Checklist do PR

- [ ] Código está formatado com Black
- [ ] Imports organizados com isort
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Commits seguem padrão semântico
- [ ] Branch atualizado com main

## 🚀 Prioridades

Áreas que precisam de contribuições:
1. **Modelos de ML** - Detecção de anomalias
2. **Dashboard** - Visualizações interativas
3. **Documentação** - Tutoriais e exemplos
4. **Testes** - Aumentar cobertura
5. **Performance** - Otimizações

## 📞 Contato

- Issues: [GitHub Issues](https://github.com/anderson-ufrj/TransparenciaBR-Analytics/issues)
- Email: anderson.henrique@ufrj.br

## 🙏 Agradecimentos

Todas as contribuições são bem-vindas e apreciadas! 🎉