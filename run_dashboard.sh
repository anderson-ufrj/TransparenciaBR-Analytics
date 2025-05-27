#!/bin/bash
# Script para executar o dashboard TransparenciaBR Analytics

echo "🚀 Iniciando TransparenciaBR Analytics Dashboard..."
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se as dependências estão instaladas
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
fi

# Verificar arquivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "   Por favor, copie .env.template para .env e configure suas credenciais."
    echo ""
    echo "   cp .env.template .env"
    echo ""
    exit 1
fi

echo "✅ Tudo pronto! Iniciando dashboard..."
echo ""
echo "📊 Acesse em: http://localhost:8501"
echo ""
echo "Para parar o servidor, pressione Ctrl+C"
echo ""

# Executar o dashboard
streamlit run src/dashboard/app.py