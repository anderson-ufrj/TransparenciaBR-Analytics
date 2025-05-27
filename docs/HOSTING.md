# 🌐 Como Hospedar o Dashboard Online (Gratuito)

Este guia mostra como disponibilizar seu dashboard Streamlit online gratuitamente.

## 🚀 Opção 1: Streamlit Community Cloud (RECOMENDADO)

### ✅ Vantagens
- **100% GRATUITO** para projetos públicos
- **Oficial do Streamlit**
- **Deploy automático** do GitHub
- **URL personalizada** (seu-app.streamlit.app)
- **Sempre online**

### 📋 Passo a Passo

1. **Crie uma conta no Streamlit Cloud**
   - Acesse: https://share.streamlit.io/
   - Faça login com sua conta GitHub

2. **Configure o projeto**
   ```bash
   # Certifique-se que requirements.txt está atualizado
   cd TransparenciaBR-Analytics
   pip freeze > requirements.txt
   
   # Crie arquivo de configuração
   mkdir .streamlit
   echo '[server]
   headless = true
   port = $PORT' > .streamlit/config.toml
   ```

3. **Adicione secrets (credenciais)**
   Crie arquivo `.streamlit/secrets.toml` (NÃO commitar!):
   ```toml
   TRANSPARENCIA_API_TOKEN = "seu_token_aqui"
   TRANSPARENCIA_EMAIL = "seu_email@exemplo.com"
   ```

4. **Deploy no Streamlit Cloud**
   - Clique em "New app"
   - Selecione seu repositório: `anderson-ufrj/TransparenciaBR-Analytics`
   - Branch: `main`
   - Main file path: `src/dashboard/app.py`
   - Clique em "Deploy!"

5. **Configure os Secrets no Streamlit Cloud**
   - Vá em Settings → Secrets
   - Cole o conteúdo do seu `.streamlit/secrets.toml`

### 🔗 URL Final
Seu app estará disponível em:
```
https://transparenciabr-analytics.streamlit.app/
```

## 🎯 Opção 2: Render.com

### ✅ Vantagens
- **Gratuito** (com limitações)
- **Deploy do GitHub**
- **Suporta Docker**

### 📋 Configuração

1. **Crie conta em render.com**

2. **Crie `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: transparenciabr-analytics
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "streamlit run src/dashboard/app.py --server.port $PORT --server.address 0.0.0.0"
       envVars:
         - key: TRANSPARENCIA_API_TOKEN
           sync: false
         - key: TRANSPARENCIA_EMAIL
           sync: false
   ```

3. **Deploy**
   - New → Web Service
   - Connect GitHub repo
   - Use render.yaml

## 🌊 Opção 3: Railway.app

### ✅ Vantagens
- **$5 grátis/mês**
- **Deploy super simples**
- **Ótima performance**

### 📋 Setup Rápido

1. **Instale Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   railway login
   railway init
   railway up
   railway domain
   ```

## 🐳 Opção 4: Fly.io

### ✅ Vantagens
- **Gratuito** para apps pequenos
- **Global deployment**
- **Ótimo para Docker**

### 📋 Configuração

1. **Crie `fly.toml`**:
   ```toml
   app = "transparenciabr-analytics"
   
   [build]
     builder = "paketobuildpacks/builder:base"
   
   [[services]]
     http_checks = []
     internal_port = 8501
     protocol = "tcp"
   
     [[services.ports]]
       handlers = ["http"]
       port = 80
   
     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

2. **Deploy**:
   ```bash
   fly auth login
   fly launch
   fly deploy
   ```

## 📱 Opção 5: Hugging Face Spaces

### ✅ Vantagens
- **100% Gratuito**
- **Focado em ML/Data Science**
- **Comunidade ativa**

### 📋 Como usar

1. **Crie um Space** em huggingface.co/spaces
2. **Escolha Streamlit** como SDK
3. **Conecte seu GitHub**
4. **Configure secrets** nas settings

## 🔧 Preparando o Projeto para Deploy

### 1. Atualize `requirements.txt`
```bash
streamlit==1.28.0
pandas==2.0.0
plotly==5.17.0
requests==2.31.0
python-dotenv==1.0.0
numpy==1.24.0
```

### 2. Configure variáveis de ambiente
```python
# src/dashboard/app.py (adicionar no início)
import os
from dotenv import load_dotenv

# Carrega .env apenas em desenvolvimento
if os.path.exists('.env'):
    load_dotenv()

# Use os.environ para acessar variáveis
API_TOKEN = os.environ.get('TRANSPARENCIA_API_TOKEN', '')
EMAIL = os.environ.get('TRANSPARENCIA_EMAIL', '')
```

### 3. Otimize recursos
```python
# Adicione cache para dados pesados
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data():
    # Seu código de carregamento
    return data

# Use session state para persistência
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

### 4. Crie arquivo de startup
```python
# startup.sh
#!/bin/bash
streamlit run src/dashboard/app.py \
  --server.port $PORT \
  --server.address 0.0.0.0 \
  --server.headless true
```

## 🎨 Personalizando a URL

### GitHub Pages para Landing Page
Embora não rode Streamlit, você pode criar uma landing page:

1. **Crie `docs/index.html`**:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>TransparenciaBR Analytics</title>
    <meta http-equiv="refresh" content="0; url=https://transparenciabr-analytics.streamlit.app/">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 50%, #F0F9FF 100%);
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        h1 { color: #047857; }
        .flag { width: 100px; margin: 20px 0; }
        .button {
            display: inline-block;
            padding: 15px 30px;
            background: #047857;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: bold;
        }
        .button:hover {
            background: #065F46;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/640px-Flag_of_Brazil.svg.png" 
             alt="Brasil" class="flag">
        <h1>TransparenciaBR Analytics</h1>
        <p>Análise inteligente de dados públicos do Portal da Transparência</p>
        <p>Você está sendo redirecionado para o dashboard...</p>
        <a href="https://transparenciabr-analytics.streamlit.app/" class="button">
            Acessar Dashboard
        </a>
        <p><small>Se não for redirecionado automaticamente, clique no botão acima.</small></p>
    </div>
</body>
</html>
```

2. **Ative GitHub Pages**:
   - Settings → Pages
   - Source: Deploy from branch
   - Branch: main, folder: /docs
   - Save

3. **URL personalizada**:
   ```
   https://anderson-ufrj.github.io/TransparenciaBR-Analytics/
   ```
   Redireciona para →
   ```
   https://transparenciabr-analytics.streamlit.app/
   ```

## 📊 Comparação das Opções

| Plataforma | Custo | Facilidade | Performance | Limites |
|------------|-------|------------|-------------|---------|
| **Streamlit Cloud** | Grátis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 1GB RAM |
| **Render** | Grátis* | ⭐⭐⭐⭐ | ⭐⭐⭐ | 512MB RAM |
| **Railway** | $5/mês grátis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 512MB RAM |
| **Fly.io** | Grátis* | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 256MB RAM |
| **HF Spaces** | Grátis | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 16GB RAM |

*Com limitações de uso

## 🚀 Deploy Rápido (5 minutos)

### Comando único para Streamlit Cloud:
```bash
# 1. Garanta que está tudo commitado
git add -A
git commit -m "🚀 deploy: preparar para Streamlit Cloud"
git push

# 2. Acesse
# https://share.streamlit.io/

# 3. New app → Selecione seu repo → Deploy!
```

## 🔒 Segurança

### ⚠️ IMPORTANTE
1. **NUNCA** commite credenciais no GitHub
2. Use **variáveis de ambiente** ou **secrets**
3. Adicione ao `.gitignore`:
   ```
   .env
   .streamlit/secrets.toml
   *.pem
   *.key
   ```

## 🎯 Recomendação Final

Para seu caso, recomendo:

1. **Streamlit Community Cloud** para o dashboard (grátis e oficial)
2. **GitHub Pages** para landing page de redirecionamento
3. **Configurar secrets** adequadamente

Isso te dará:
- ✅ Dashboard sempre online
- ✅ URL profissional
- ✅ Zero custo
- ✅ Deploy automático do GitHub
- ✅ Ótima performance

## 📝 Checklist de Deploy

- [ ] requirements.txt atualizado
- [ ] Variáveis de ambiente configuradas
- [ ] Secrets não estão no código
- [ ] .gitignore configurado
- [ ] README com instruções
- [ ] Imagens otimizadas
- [ ] Cache implementado
- [ ] Testes passando

Pronto! Seu dashboard estará online e acessível para todos! 🎉